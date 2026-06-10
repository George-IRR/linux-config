# 01: POST Fault Analysis and Power Subsystem Mapping

Root-cause analysis documentation detailing hardware structural failures extracted from the iRMC event registry for the Fujitsu PRIMERGY TX200 S6 chassis architecture.

---

## Diagnostic Matrix

| Code | Severity | Component | Error Signature | Root Cause / Operational Impact |
| --- | --- | --- | --- | --- |
| **190014** | Critical | BIOS | `POST - No usable system memory` | Fatal failure during the early memory sizing routine. Memory bus initialization dropped completely. |
| **130001** | Critical | BIOS | `Error during POST code 0x28` | Memory controller execution block. The system fails to train, map, or reference installed DIMM modules. |
| **070002** | Critical | PSU1 | `'PSU1': Power supply failed` | Complete component failure or shutdown of the internal power circuit loop. |
| **040003** | Major | FAN PSU1 | `'FAN PSU1': Redundant fan failed` | Cooling fan stoppage inside the power supply container, precipitating rapid thermal breakdown. |
| **020000** | Critical | iRMC S2 | `Power unit AC lost` | Direct drop in voltage input or severance of AC connection path to the physical PSU module. |

---

## Fault Analysis & Interdependency Mechanics

### 1. The Power-to-Memory Failure Chain

The logical synchronization of the logs highlights that memory dropouts (`Code 190014`) are secondary symptoms of underlying infrastructure failures within the power supply framework.

* **Thermal Escalation Timeline:** The initial structural failure sequence began with the death of `FAN PSU1` (`Code 040003`). Lacking forced convection cooling, the internal components reached critical thermal saturation points under load. This led to immediate circuit degradation, triggering a hardware state failure on `PSU1` (`Code 070002`).
* **Voltage Instability:** When a primary or redundant power module collapses under thermal stress, internal voltage rails (especially the `+12V` and `+3.3V` lines feeding the motherboard VRMs) experience severe noise, ripple, or sudden voltage sag. Memory training sequences executed during POST require absolute voltage precision to tune signal timings across high-frequency trace buses. Electrical fluctuations on these rails cause memory bus initialization routines to abort instantly, causing the system to throw POST error code `0x28`.

### 2. Historical Redundancy Loss

Historical logs document preceding component drops: `FAN PSU2` and `PSU2 AC Lost` configurations failed globally in December 2025. If `PSU2` was never structurally replaced or re-serviced, the system completely lacks a secondary power vector, causing the physical failure of `PSU1` to leave the system motherboard running on volatile, un-stabilized residual power or partial phases.

---

## Step-by-Step Hardware Isolation Protocol

When a machine fails to initialize past POST code `0x28`, apply a systematic hardware breakdown to determine whether the fault stems from contaminated paths, a single dead module, or total VRM degradation on the board:

1. **Purge Residual Charge:** Sever all incoming AC utility lines from both `PSU1` and `PSU2`. Hold down the physical power button on the server chassis front panel for 30 consecutive seconds to drain internal filter capacitors on the motherboard.
2. **Isolate Compromised Power Units:** Extract the physically compromised power module (`PSU1`) entirely from its chassis bay slot to guarantee it cannot pollute the shared internal PMBus communications lines or short-circuit shared power backplanes.
3. **Clean the Memory Interface:** Extract all installed DDR3 memory modules. Utilizing filtered, dry compressed air, thoroughly blow out the DIMM slots to clear micro-particulates or conductive dust buildup. Clean the physical contact fingers of the memory modules using isopropyl alcohol (minimum 99% purity) and let them dry completely.
4. **Execute Minimal Channel Mapping:** Refer to the silk-screened memory matrix map printed on the chassis casing plate. Identify **Channel A, Slot 1 for Processor 1 (CPU1)**. Populate **exactly one single verified RAM module** into this primary slot. Leave all other memory paths vacant.
5. **Re-initialize Testing Phase:** Plug an AC cord into the remaining active power unit (`PSU2`, verifying a solid green status LED). Initiate a power state transition and trace the iRMC event logger:
* *If the machine bypasses error code 0x28:* The problem points to a single defective RAM module among those removed, or an invalid interleaved memory channel layout topology. Reintroduce modules incrementally to flag the broken hardware stick.
* *If error code 0x28 remains persistent:* Replace the single installed module with a secondary replacement module. If the initialization routine consistently aborts across multiple discrete modules in the primary slot, the issue stems from systemic degradation of the CPU memory controller or physical trace damage on the motherboard.