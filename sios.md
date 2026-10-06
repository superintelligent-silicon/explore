# SIOS — Silicon OS / Superintelligent OS

> Plain-text summary of https://exploresuperintelligence.online/sios/ — a compact, local-first mini-OS preview from Superintelligent Silicon that runs in your web browser. Live shell: https://exploresuperintelligence.online/sios/shell/ · Source (MIT): https://github.com/superintelligent-silicon/sios

## What it is

SIOS (Silicon OS / Superintelligent OS) is a small, local-first utility layer: files, keys, calculator, calendar, notes, and settings — interoperable, exportable, calm. It is built to open in a page or (later) as a small desktop app. It is not a cloud desktop, not a replacement for macOS / Windows / Linux, and not a hosted service you must sign up for.

## Status (Phase 1a, early preview)

Live in the in-browser shell:

- **Files** — virtual file system stored in IndexedDB on your device; JSON import/export
- **Notes** — Markdown (`.md`) notes saved as files under `/Notes`; plain-text editor (no HTML rendering)
- **Settings** — theme, Keys idle lock timeout, storage status, backup
- **Keys** — on-device Web Crypto vault (PBKDF2 600k iterations + AES-GCM). **Not audited** — use for non-critical data only
- **Calc** — calculator with history and Save to Files
- **Calendar** — month view, events, JSON import/export
- **Backup** — clearly labeled **unencrypted** ZIP export/import
- Local data bus for explicit hand-offs between modules; strict Content Security Policy

No accounts. Data stays on the device by default; the shell does not upload your data or collect keys. Nothing is productized as a download yet.

## Principles

Local-first · small footprint · interoperable modules · plain export formats · honest security claims.

## Links

- SIOS page: https://exploresuperintelligence.online/sios/
- Live shell: https://exploresuperintelligence.online/sios/shell/
- Source and docs: https://github.com/superintelligent-silicon/sios (vision: docs/VISION.md, Keys threat model: docs/KEYS.md)
- What's shipping: https://exploresuperintelligence.online/shipping/
- Explore Superintelligence home: https://exploresuperintelligence.online/
- Contact Superintelligent Silicon: https://superintelligentsilicon.com/#contact
