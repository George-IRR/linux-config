# Documentation & Contribution Standards

This repository maintains hardened, production-ready configurations, operational runbooks, and troubleshooting playbooks. All contributions and generated guides must adhere to the structural, technical, and privacy standards defined below.

---

## 1. Directory Structure & File Naming Conventions

- **Directory Placement:** Guides must reside inside their relevant functional domain (`server-management/`, `software-management/`, `system-optimizations/`, `backup-operations/`, `hardware-diagnostics/`, etc.).
- **File Naming:**
  - Format: `XX_UPPERCASE_DESCRIPTION.md`
  - `XX` is a sequential two-digit zero-padded index incrementing the existing count in that folder (e.g., `09_SSH_KEY_AUTHENTICATION_HARDENING.md`).
  - Use concise, descriptive, uppercase slugs separated by underscores.

---

## 2. Privacy & Sanitization Rules (Zero-Leak Policy)

Documentation must be strictly generic and safe for public repositories. Never commit personal or environment-specific identifiers:

| Target Entity | Forbidden (Specific) | Permitted (Standardized Placeholder) |
| :--- | :--- | :--- |
| **Usernames** | `george`, `root-george` | `<user>`, `$USER` |
| **Local Paths** | `/home/george/...` | `~/...`, `$HOME/...`, `/home/<user>/...` |
| **Hostnames** | `george-desktop`, `t630-2-server` | `<client-host>`, `<server-host>`, `localhost` |
| **IP Addresses** | `100.72.145.102`, `192.168.0.100` | `<server-ip>`, `192.168.1.X`, `<client-ip>` |
| **Credentials** | Plain passwords, actual public/private keys | `REDACTED`, `<auth-token>`, `<ssh-public-key>` |

---

## 3. Document Structure Template

Every guide must strictly adhere to the following scaffolding:

1. **Title & Synopsis:**
   - Single `# Title` header.
   - One concise introductory paragraph defining the technical scope, problem statement, and operating context.
2. **Core Operational Steps:**
   - Numbered sections using Markdown `## 1. Section Title`.
   - Commands enclosed in language-specific code blocks (`bash`, `ini`, `yaml`, `systemd`) with copy-pasteable defaults.
   - Brief bullet points explaining non-standard flags.
3. **Diagnostics & Validation:**
   - Explicit verification commands paired with a literal `Expected Output` block.
4. **Best Practices (Do's and Don'ts):**
   - Actionable list covering operational risks, edge cases, and rollback precautions.

---

## 4. Automated Guide Generation (`generate_guide.py`)

New runbooks should be scaffolded via the root automated generator:

```bash
./generate_guide.py "<Brief Problem Summary>"

```

* **Zero-Prompt Placement:** The script automatically matches keywords (`ssh`, `docker`, `backup`, `pipewire`) to the proper directory without manual prompts.
* **Parser Collisions:** Script generators must isolate triple backticks into independent variables (`ticks = "```"`) to prevent early Markdown termination inside code fences.

---

## 5. Repository Index Registration

Any new guide added to a subdirectory must be registered in the root `README.md` index under its corresponding section:

* Format: `* [`.md`](<category>/<FILENAME>.md) - <Single scope sentence summarizing technical>.`
* Maintain sequential index order matching the file numbers.

---

## 6. Commit Conventions

Contributions must follow the Conventional Commits specification:

* `docs(<domain>): add <guide-name>` (e.g., `docs(server-management): add SSH key auth hardening guide`)
* `fix(<domain>): resolve <issue>`
* `refactor(tooling): update automated guide generator`