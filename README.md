# alcatras_notes

My personal [Obsidian](https://obsidian.md) knowledge base — a **Zettelkasten** of study
notes, kept in git and backed up on GitHub.

The notes are written mostly in **Russian**, with a fair amount of English terminology.
There is no code here — the repository is the notes, their attachments and the Obsidian
configuration.

## What's inside

Roughly **310 markdown notes**, dominated by Cybersecurity, plus a few other tracks:

| Area | Folder | Notes |
| --- | --- | --- |
| Cybersecurity (main) | `alcatras/Cybersecurity/` | ~290 |
| Fleeting notes / tasks / problems | `alcatras/Flutting notes/` | ~13 |
| Self-development & study techniques | `alcatras/self development/` | ~5 |
| Index / map-of-content notes | `alcatras/State notes/` | ~1 |
| Misc | `alcatras/CROC/` | ~1 |

The Cybersecurity section is itself a deep tree, e.g.:

- **Computer Networks** — physical/data-link/network/transport layers, routing, MAC,
  TCP/UDP/QUIC/SCTP/DNS/HTTP/TLS, congestion control.
- **Operating Systems** — processes & threads, system calls, memory, scheduling.
- **File Systems** — files, directories, implementation (FAT, UNIX V7, journalling, LFS, VFS),
  management & optimisation.
- **I/O** — hardware principles, drivers, interrupt handling, DMA.
- **Computer Architecture** — CPU, cache, memory hierarchy.
- **SOC** — triage playbooks, frameworks (MITRE, Cyber Kill Chain, Pyramid of Pain),
  defence tooling (SIEM, EDR, IDS, SOAR).
- **CTF** — crypto (RSA, DH, Caesar/XOR), web (CORS, CSRF, SQLi, SSTI, cookies), tooling.

## How it's organised

The vault follows Zettelkasten conventions:

- **Linking** — ideas are connected with Obsidian `[[wikilinks]]` (~210 of the notes use them).
  Index / map-of-content notes (e.g. `State notes/Cybersecurity.md`) act as entry points into
  a topic.
- **No front matter / metadata** — notes are plain markdown; structure comes from folders and
  links, not YAML.
- **Attachments** — images and diagrams live in `Cache/` and are embedded as
  `![[Cache/Pasted image ....png]]`.
- **Canvas** — a handful of `.canvas` files hold visual diagrams (network flows, FS layouts,
  playbooks).

## Repository layout

```
alcatras_notes/
├── alcatras/              # ← the vault: open THIS folder in Obsidian
│   ├── .obsidian/         # vault config, core plugins, hotkeys
│   ├── Cybersecurity/     # the bulk of the notes
│   ├── Flutting notes/    # fleeting / task / problem notes
│   ├── self development/
│   ├── State notes/       # index notes
│   ├── CROC/
│   └── Cache/             # attachments (images, canvas)
└── .obsidian/             # workspace/appearance config for the parent folder
```

## Usage

```bash
git clone https://github.com/daklik-not/alcatras_notes.git
```

Then in Obsidian: **Open folder as vault** → pick the `alcatras/` directory.

The `.obsidian/` config is committed on purpose, so plugins, hotkeys and appearance travel
with the repo. If you clone only to read the notes, you can ignore it — plain markdown works
anywhere (GitHub, any editor, any markdown viewer).

## Notes

- The notes are personal study material and may contain errors, half-finished thoughts and
  rough formatting. Treat them as working notes, not as a reference.
- Only git-managed markdown is versioned meaningfully; Obsidian's `workspace.json` (open tabs,
  pane layout) changes constantly with use, so expect noise in diffs from `.obsidian/`.
- See the per-directory index notes for the intended reading order.
