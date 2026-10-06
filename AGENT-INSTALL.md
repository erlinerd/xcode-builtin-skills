# Agent Setup Instructions

This repository (`erlinerd/xcode-builtin-skills`) archives the 10 built-in Agent skills bundled with Xcode 27 (plus one self-written router skill) and the MCP tools they depend on. If you are reading this, your task is to install, configure and verify everything end to end. Follow the steps in order and report the outcome of each.

## Step 1 — Install the skills

Run:

```bash
npx skills add erlinerd/xcode-builtin-skills
```

This installs all 11 skills into your host's skill directory. The three groups are:

- `ask`: `ask-xcode` (self-written router that dispatches requests to the two groups below; not Apple content)
- `xcode-integration`: `translation`, `translation-coordinator` (String Catalog translation)
- `ide-intelligence-chat`: `swiftui-specialist`, `swiftui-whats-new-27`, `app-intents-specialist`, `app-intents-whats-new-27`, `adopt-c-bounds-safety`, `audit-xcode-security-settings`, `building-document-based-swiftui-applications`, `uikit-app-modernization`

## Step 2 — Configure the Xcode MCP

The two `xcode-integration` skills depend on the MCP bridge bundled with Xcode 27+. Check whether an MCP server with `command: "xcrun"` and `args: ["mcpbridge"]` already exists in this host's MCP configuration.

- **If it exists**: do nothing.
- **If it does not**: add it. For Claude Code, either edit `~/.claude.json`:

```json
{
  "mcpServers": {
    "xcode": {
      "type": "stdio",
      "command": "xcrun",
      "args": ["mcpbridge"],
      "env": {}
    }
  }
}
```

or run:

```bash
claude mcp add xcode --transport stdio xcrun mcpbridge
```

After adding it, remind the user to restart the session so the tools load.

## Step 3 — Verify and report

Confirm and report both of the following:

1. The skill list contains the 11 skills listed in Step 1 (including the `ask-xcode` router).
2. The MCP tools are available: `StringCatalogContext`, `StringCatalogEdit`, `StringCatalogRead`, `LocalizationPlanner`.

If the MCP tools are missing, tell the user to open Xcode once (to accept the license) and confirm `xcrun mcpbridge` runs standalone, then retry.

## Rules for translation tasks

When the user asks you to translate Xcode String Catalogs (`.xcstrings`):

- Load the `xcode-integration:translation` skill **before** calling `StringCatalogContext` or `StringCatalogEdit`.
- Load the `xcode-integration:translation-coordinator` skill **before** calling `StringCatalogRead` or `LocalizationPlanner`.
- Access `.xcstrings` files **only** through these MCP tools — never read or write them directly.
- Pass locale identifiers verbatim (given `zh-TW`, use `zh-TW` — never normalize it).
