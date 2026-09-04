# Shotcut HDR (10-bit HLG) Export & AMD Optimization Guide

Technical guide for configuring, editing, and rendering 10-bit HDR (HLG / Rec.2020) video in Shotcut on Linux (Ubuntu / AMD Ryzen & Radeon), preventing color matrix corruption and encoder crashes.

---

## 1. Performance & Timeline Optimization (AMD Hardware)

### Timeline & UI Rendering
* **Display Method:** Go to `Settings` -> `Display Method` -> select **Vulkan** (or **Direct3D11** on Windows). Eliminates OpenGL driver overhead and latency on AMD Radeon graphics.
* **Preview Scaling:** Set `Settings` -> `Preview Scaling` -> **360p** or **540p** while editing for responsive scrubbing.
* **Disable Before Export:** Ensure `Preview Scaling` is set to **None** prior to the final export to prevent downscaled rendering artifacts.

---

## 2. Diagnostics: Why HDR Tags Fail & Neon Green Artifacts Occur

### Causes of Green / Corrupted Colors
1. **Forced 8-bit Fallback:** If the internal engine runs in 8-bit (`yuv420p`) but Rec.2020 VUI tags are forced, the U and V chroma channels misalign, producing a neon-green cast.
2. **Incorrect Transfer Curve:** `color_transfer=bt2020-10` is an SDR gamma curve. Mobile devices (iOS / Android) require an explicit **HLG** (`arib-std-b67`) or **PQ** (`smpte2084`) curve to trigger the HDR display panel.

### Verify System Encoder Capabilities
Check if the local FFmpeg build supports native 10-bit HEVC encoding:

```bash
ffmpeg -f lavfi -i color=black:s=100x100:d=1 -c:v libx265 -pix_fmt yuv420p10le -f null -

```

* If the output shows `build info ... 10bit` and `Main 10 profile`, 10-bit HEVC encoding is fully supported.

---

## 3. Direct Export Configuration in Shotcut (10-bit HLG)

1. **Color Space:** `Settings` -> `Video Mode` -> select a profile with the **HLG** suffix (e.g., *HD 1080p 30 fps HLG* or *Rec. 2020 HLG*).
2. **Processing Mode:** `Settings` -> `Processing Mode` -> check **Native 10-bit CPU**.
3. **Export Panel -> Advanced**:
* **Video:** Uncheck `Use hardware encoder` (avoids `hevc_vaapi exit code 11` segfaults).
* **Codec:** Select `libx265`. Under **Pixel format**, select `yuv420p10le`.
* **Other:** Replace the existing configuration with:



```ini
vtag=hvc1
preset=medium
vprofile=main10
pix_fmt=yuv420p10le
movflags=+faststart
color_primaries=bt2020
color_trc=arib-std-b67
colorspace=bt2020nc
x265-params=colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc

```

---

## 4. Alternative Master Workflow (Master ProRes -> FFmpeg)

If Shotcut is running inside an isolated sandbox (e.g., Snap) with an internal `libx265` compiled strictly for 8-bit:

### Step 1: Export a 10-bit Master from Shotcut

* In **Export** -> **Presets** -> **intermediate** -> select **ProRes**.
* Under **Advanced** -> **Codec**, verify that **Pixel format** is set to `yuv422p10le`.
* Render the file (e.g., `master_10bit.mov`).

### Step 2: Final HDR Encode via Terminal FFmpeg

```bash
ffmpeg -i master_10bit.mov \
  -c:v libx265 -crf 20 -preset fast \
  -pix_fmt yuv420p10le \
  -color_primaries bt2020 \
  -color_trc arib-std-b67 \
  -colorspace bt2020nc \
  -x265-params "colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc" \
  -tag:v hvc1 \
  -c:a aac -b:a 256k \
  output_final_hdr.mp4

```

---

## 5. Instant Remux: Fix HDR Metadata in 2 Seconds (No Re-encoding)

If a file has already been rendered in 10-bit (`yuv420p10le`) but the mobile device does not trigger HDR because of `color_transfer=bt2020-10`, remux the bitstream tags without re-encoding:

```bash
ffmpeg -i input_10bit.mp4 -c copy \
  -bsf:v "hevc_metadata=colour_primaries=9:transfer_characteristics=18:matrix_coefficients=9" \
  -color_trc arib-std-b67 \
  -color_primaries bt2020 \
  -colorspace bt2020nc \
  -tag:v hvc1 \
  output_hdr_fixed.mp4

```

### Validate Metadata

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,pix_fmt,color_space,color_transfer,color_primaries \
  -of default=noprint_wrappers=1 output_hdr_fixed.mp4

```

**Expected Output:**

```text
codec_name=hevc
pix_fmt=yuv420p10le
color_space=bt2020nc
color_transfer=arib-std-b67
color_primaries=bt2020

```

---

## 6. Best Practices (Do's and Don'ts)

### DO:

* Always specify `-tag:v hvc1` for MP4/MOV containers intended for mobile hardware decoders (iOS and Android).
* Verify with `ffprobe` that `pix_fmt` is `yuv420p10le` before applying HDR metadata flags.
* For quick local testing without data transfer cables, use **LocalSend** (`org.localsend.localsend_app`) or VLC's built-in Wi-Fi sharing feature.

### DON'T:

* **Do not re-encode an 8-bit file to 10-bit:** Clipped highlights and crushed shadows cannot be recovered; players will display washed-out fake HDR with severe color banding.
* **Do not use `hevc_vaapi` for 10-bit rendering in Shotcut** on generic Linux desktop stacks (causes `exit code 11 / Segfault` when transferring software frames).
* **Do not use standard `python3 -m http.server` for large video playback:** It lacks HTTP 206 Partial Content (Range request) support and crashes with `BrokenPipeError` when mobile players request byte chunks.
* **Do not use `bt2020-10` as a transfer characteristic:** It is treated as standard SDR by mobile OS image engines.
