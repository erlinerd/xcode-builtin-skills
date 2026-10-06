# Xcode Built-in Skills

English | [简体中文](README.md)

Full-text archive of the 10 Agent skills bundled with Xcode 27 (plus one self-written router), organized for the `skills` CLI and installable into any Agent-Skills-compatible host (Claude Code, Codex, Cursor, …) with one command. Sourced from the official prompt files inside `/Applications/Xcode.app`; body content is byte-identical.

## Skills

| Skill | What it does | Install |
|---|---|---|
| [translation](skill/xcode-integration/translation/) | Translate String Catalog strings via the MCP tools, one at a time, with 56 locale style guides | `npx skills add erlinerd/xcode-builtin-skills/skill/xcode-integration/translation` |
| [translation-coordinator](skill/xcode-integration/translation-coordinator/) | Orchestrate whole-project localization: prepare → fetch keys → delegate batches → verify | `npx skills add erlinerd/xcode-builtin-skills/skill/xcode-integration/translation-coordinator` |
| [swiftui-specialist](skill/ide-intelligence-chat/swiftui-specialist/) | Authoritative SwiftUI best practices (animation, @Observable, ForEach, localization) | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/swiftui-specialist` |
| [swiftui-whats-new-27](skill/ide-intelligence-chat/swiftui-whats-new-27/) | SwiftUI '27 what's new | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/swiftui-whats-new-27` |
| [app-intents-specialist](skill/ide-intelligence-chat/app-intents-specialist/) | Authoritative App Intents guidance | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/app-intents-specialist` |
| [app-intents-whats-new-27](skill/ide-intelligence-chat/app-intents-whats-new-27/) | App Intents '27 what's new | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/app-intents-whats-new-27` |
| [adopt-c-bounds-safety](skill/ide-intelligence-chat/adopt-c-bounds-safety/) | Incrementally adopt `-fbounds-safety` in C projects | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/adopt-c-bounds-safety` |
| [audit-xcode-security-settings](skill/ide-intelligence-chat/audit-xcode-security-settings/) | Audit security hardening build settings (PAC, stack zero-init, …) | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/audit-xcode-security-settings` |
| [building-document-based-swiftui-applications](skill/ide-intelligence-chat/building-document-based-swiftui-applications/) | Document-based SwiftUI apps | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/building-document-based-swiftui-applications` |
| [uikit-app-modernization](skill/ide-intelligence-chat/uikit-app-modernization/) | Modernize UIKit apps | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/uikit-app-modernization` |

> Also included: the self-written router skill [ask-xcode](skill/ask/ask-xcode/) — dispatches requests to the 10 skills above. Not Apple content. The bulk-install command includes it (11 skills total).

Or install all 11 at once:

```bash
npx skills add erlinerd/xcode-builtin-skills
```

## Copy-paste for your agent

Send this single line to your agent — it will read [AGENT-INSTALL.md](AGENT-INSTALL.md) and handle installation, configuration and verification on its own:

```text
Fetch the file AGENT-INSTALL.md from the GitHub repo erlinerd/xcode-builtin-skills (https://github.com/erlinerd/xcode-builtin-skills/blob/main/AGENT-INSTALL.md) and follow its instructions to install and configure the Xcode built-in skills.
```

(If the repo is already cloned locally, just say: "Read AGENT-INSTALL.md and follow it".)

## Prerequisites

- **Xcode MCP**: `translation` / `translation-coordinator` depend on the MCP bridge bundled with Xcode 27 (`xcrun mcpbridge`). See [mcp/setup.md](mcp/setup.md) for configuration, tool overview and activation rules.
- **ide-intelligence-chat group**: no MCP dependency — install and use.

## Layout

```
skill/                      # skills-CLI-compatible: skill/<group>/<name>/SKILL.md
├── ask/                    # the ask-xcode router (self-written, dispatches to the two groups below)
├── xcode-integration/      # the translation pair (official namespace)
└── ide-intelligence-chat/  # 8 specialist skills (group name from framework name, kebab-case)
mcp/                       # Xcode MCP setup + tool overview & activation rules (setup.md)
```

Provenance of the groups:

- `xcode-integration`: from `IDEXCStringsSupport.framework/.../Skills/` — official prompts as-is (the two SKILL.md files only gained the minimal frontmatter required by the skills CLI; bodies untouched).
- `ask` group: `ask-xcode` is a router skill written for this repo, not Apple content, excluded from the fidelity stats.
- `IDEIntelligenceChat`: from `IDEIntelligenceChat.framework/.../Resources/` — `<name>.idechatprompttemplate` → `SKILL.md`, `<name>-ref-*.md.packaged` → `references/<topic>.md`.

## Fidelity to the official files

Per-file sha256 against the files inside `Xcode.app`: **all 141 sourced files match** (139 byte-identical + the 2 translation SKILL.md files differing only by frontmatter, bodies identical). The only two differences are the 4-line frontmatter (`name`/`description`) added to the two translation SKILL.md files to satisfy the skills CLI contract — bodies are unchanged.

## Updating

After an Xcode upgrade, re-sync with:

```bash
scripts/sync-from-xcode.py            # defaults to /Applications/Xcode.app; pass a custom path to override
```

The script auto-detects added/removed skills and references, preserves the translation SKILL.md frontmatter, and prints a byte-level fidelity check at the end.
