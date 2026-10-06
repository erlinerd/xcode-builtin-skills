# Xcode Built-in Skills

[English](README.en.md) | 简体中文

Xcode 27 内置 Agent 技能全文存档（10 个官方技能 + 1 个自写路由），按 `skills` CLI 规范组织，可一键安装到任意支持 Agent Skills 的宿主（Claude Code、Codex、Cursor 等）。内容源自 `/Applications/Xcode.app` 内的官方提示词文件，正文字节级一致。

## 技能列表

| 技能 | 说明 | 安装 |
|---|---|---|
| [translation](skill/xcode-integration/translation/) | 经 MCP 工具逐条翻译 String Catalog 文案，含 56 种语言风格指南 | `npx skills add erlinerd/xcode-builtin-skills/skill/xcode-integration/translation` |
| [translation-coordinator](skill/xcode-integration/translation-coordinator/) | 整项目本地化编排：准备 → 取 key → 分批派发子代理 → 验证 | `npx skills add erlinerd/xcode-builtin-skills/skill/xcode-integration/translation-coordinator` |
| [swiftui-specialist](skill/ide-intelligence-chat/swiftui-specialist/) | SwiftUI 权威最佳实践（动画、@Observable、ForEach、本地化） | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/swiftui-specialist` |
| [swiftui-whats-new-27](skill/ide-intelligence-chat/swiftui-whats-new-27/) | SwiftUI 2027 版新特性 | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/swiftui-whats-new-27` |
| [app-intents-specialist](skill/ide-intelligence-chat/app-intents-specialist/) | App Intents 权威指南 | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/app-intents-specialist` |
| [app-intents-whats-new-27](skill/ide-intelligence-chat/app-intents-whats-new-27/) | App Intents 2027 版新特性 | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/app-intents-whats-new-27` |
| [adopt-c-bounds-safety](skill/ide-intelligence-chat/adopt-c-bounds-safety/) | 在 C 项目中渐进采用 `-fbounds-safety` | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/adopt-c-bounds-safety` |
| [audit-xcode-security-settings](skill/ide-intelligence-chat/audit-xcode-security-settings/) | 安全加固设置审计（指针认证、栈零初始化等） | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/audit-xcode-security-settings` |
| [building-document-based-swiftui-applications](skill/ide-intelligence-chat/building-document-based-swiftui-applications/) | 文档型 SwiftUI 应用 | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/building-document-based-swiftui-applications` |
| [uikit-app-modernization](skill/ide-intelligence-chat/uikit-app-modernization/) | UIKit 应用现代化改造 | `npx skills add erlinerd/xcode-builtin-skills/skill/ide-intelligence-chat/uikit-app-modernization` |

> 另有自写的路由技能 [ask-xcode](skill/ask/ask-xcode/)：把请求分发到上述 10 个技能的入口，非 Apple 内容。一次性安装命令包含它（共 11 个技能）。

一次性装全部 11 个：

```bash
npx skills add erlinerd/xcode-builtin-skills
```

## 复制给 Agent

把这一行发给你的 Agent 即可，它会读取 [AGENT-INSTALL.md](AGENT-INSTALL.md) 并自动完成安装、配置与验证：

```text
Fetch the file AGENT-INSTALL.md from the GitHub repo erlinerd/xcode-builtin-skills (https://github.com/erlinerd/xcode-builtin-skills/blob/main/AGENT-INSTALL.md) and follow its instructions to install and configure the Xcode built-in skills.
```

（若已克隆仓库到本地，直接说「读取 AGENT-INSTALL.md 并执行」即可。）

## 使用前提

- **Xcode MCP**：`translation` 与 `translation-coordinator` 依赖 Xcode 27 自带的 MCP 桥（`xcrun mcpbridge`），配置方法见 [mcp/setup.md](mcp/setup.md)（含工具一览与激活规则）。
- **ide-intelligence-chat 组**：不依赖 MCP 工具，装上即可用。

## 目录结构

```
skill/                      # skills CLI 兼容：skill/<组>/<技能名>/SKILL.md
├── ask/                    # ask-xcode 路由技能（自写，分发到下面两组）
├── xcode-integration/      # 翻译对（官方命名空间）
└── ide-intelligence-chat/  # 8 个专家技能（组名取自框架名，小写中横线）
mcp/                        # Xcode MCP 配置 + 工具一览与激活规则（setup.md）
```

各组来源：

- `ask` 组：`ask-xcode` 为本仓库自写的路由技能，非 Apple 内容，不在一致性统计内。
- `xcode-integration` 组：`IDEXCStringsSupport.framework/.../Skills/`，官方提示词原样（两个 SKILL.md 仅补了 skills CLI 所需的最小 frontmatter，正文未动）。
- `ide-intelligence-chat` 组：组名取自官方框架 `IDEIntelligenceChat.framework`（小写中横线化），来自 `.../Resources/`，原 `<名>.idechatprompttemplate` → `SKILL.md`，`<名>-ref-*.md.packaged` → `references/<题>.md`。

## 与官方文件的一致性

逐文件 sha256 对比 `Xcode.app` 内源文件：**141 个文件全部与源一致**（139 个字节级相同 + 2 个翻译 SKILL.md 仅 frontmatter 差异，正文相同）；唯二差异是两个翻译技能的 SKILL.md 增加了 4 行 frontmatter（`name`/`description`，为满足 skills CLI 契约），正文未改动。

## 更新

Xcode 升级后重新同步：

```bash
scripts/sync-from-xcode.py            # 默认 /Applications/Xcode.app，也可传自定义路径
```

脚本会自动发现新增/删除的技能与参考文件，保留翻译 SKILL.md 的 frontmatter，并在结束时输出与官方源的字节级校验结果。
