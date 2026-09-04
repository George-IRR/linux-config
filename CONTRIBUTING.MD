# Documentation & Contribution Standards

This repository maintains hardened, production-ready configurations, operational runbooks, and troubleshooting playbooks. All contributions and generated guides must adhere to the structural, technical, and privacy standards defined below.

---

## 1. Directory Structure & File Naming Conventions

* **Directory Placement:** Guides must reside inside their relevant functional domain (`software-management/`, `system-optimizations/`, `backup-operations/`, `hardware-diagnostics/`, etc.).
* **File Naming:**
  * Format: `XX_UPPERCASE_DESCRIPTION.md`
  * `XX` is a sequential two-digit zero-padded index incrementing the existing count in that folder (e.g., `08_SHOTCUT_HDR_10BIT_EXPORT.md`).
  * Use concise, descriptive, uppercase slugs separated by underscores.

---

## 2. Privacy & Sanitization Rules (Zero-Leak Policy)

Documentation must be strictly generic and safe for public repositories. Never commit personal or environment-specific identifiers:
* **Usernames & Paths:** Never use absolute machine paths like `/home/george/...`. Use generic paths (`~/...`), variables (`$HOME/...`), or placeholders (`<user>`).
* **Network Identifiers:** Do not hardcode specific local LAN IPs (e.g., `192.168.0.100`), external public IPs, MAC addresses, or custom local hostnames. Use generic equivalents (`192.168.1.X`, `<host-ip>`, `localhost`).
* **Credentials & Tokens:** Replace all actual passwords, private keys, API hashes, or server serial numbers with standardized placeholders (e.g., `REDACTED`, `<auth-token>`).

---

## 3. Document Structure Template

Every guide must follow this baseline scaffolding:

1. **Title & Synopsis:**
   * Single `# Title` header.
   * One concise introductory paragraph defining the scope, problem, and target environment (OS, hardware, or kernel context).

2. **Core Operational Sections:**
   * Numbered sections using Markdown `## 1. Section Title`.
   * Commands enclosed in language-specific code blocks (`bash`, `ini`, `yaml`, `systemd`) with actionable flags.
   * Avoid generic placeholder commands; provide copy-pasteable blocks using sane defaults.

3. **Diagnostics & Validation:**
   * Include verification commands (e.g., `systemctl status`, `ffprobe`, `curl -I`) and provide the literal `Expected Output` block so results can be evaluated immediately.

4. **Best Practices (Do's and Don'ts):**
   * Conclude with a bulleted list covering edge cases, pitfalls to avoid, and safe operational guidelines.

---

## 4. Repository Index Registration

Any new guide added to a subdirectory must be registered in the root `README.md` index under its corresponding section:

* Format: `* [`<FILENAME>.md`](<category>/<FILENAME>.md) - <Single sentence summarizing technical scope>.`
* Maintain alphabetical or numerical sorting consistent with the existing catalog.

---

## 5. Technical Tone

* Use concise, imperative technical English.
* Lead directly with configurations and terminal commands; omit conversational greetings or meta-text.
* Explain the *why* behind non-obvious kernel, codec, or driver flags in brief bullet points below commands.