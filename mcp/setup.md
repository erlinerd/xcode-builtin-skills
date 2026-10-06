# 如何配置 Xcode MCP

Xcode 27 自带官方 MCP 桥接（实测于 Xcode 27.0 / 27A266a）（`xcrun mcpbridge`），无需安装第三方包。本仓库 skill 所依赖的 StringCatalogContext / StringCatalogEdit / StringCatalogRead / LocalizationPlanner 等工具均由它提供。

## 前置要求

- macOS + Xcode 27 及以上（首次使用在 Xcode 里打开一次项目，完成许可与组件安装）
- 命令行可直接运行：`xcrun mcpbridge`

## 配置方式（stdio）

### Claude Code

`~/.claude.json` 顶层 `mcpServers`（本机实测生效的配置）：

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

等价命令行：

```bash
claude mcp add xcode --transport stdio xcrun mcpbridge
```

### 其他支持 MCP 的宿主

通用 stdio 约定一致：`command = xcrun`，`args = ["mcpbridge"]`，无需环境变量。

## 验证

1. 重启宿主会话后，工具列表应出现 `mcp__xcode__*` 前缀的工具（BuildProject、StringCatalogContext 等）。
2. 翻译工具的调用前置：StringCatalogContext / StringCatalogEdit 须先加载 `xcode-integration:translation` 技能；StringCatalogRead / LocalizationPlanner 须先加载 `xcode-integration:translation-coordinator` 技能——规则写在工具描述里，见同目录各工具文档。

## 技能依赖的工具一览

4 个工具均由 `xcrun mcpbridge` 提供；每个工具都要求**调用前先激活对应技能**（写在工具描述里）：

| 工具 | 前置技能 | 用途 |
|---|---|---|
| `StringCatalogContext` | `xcode-integration:translation` | 取某条字符串的源文与上下文（注释/相似串/代码位置/复数要求） |
| `StringCatalogEdit` | `xcode-integration:translation` | 写入翻译；4 种形态：`translation` / `stringSetTranslation` / `templateTranslation`（复数模板）/ `variationTranslation`（顶层复数·设备·宽度变体） |
| `StringCatalogRead` | `xcode-integration:translation-coordinator` | 按 locale 和翻译状态（new/needs_review/translated/machine_translated）取 string key，支持分页 |
| `LocalizationPlanner` | `xcode-integration:translation-coordinator` | 翻译前的项目就绪准备：加语言、创建 String Catalog |

关键参数规则：locale 标识符照原样传（给 `zh-TW` 就传 `zh-TW`，禁止规范化）；写入翻译时用目标语言的排版引号（德语 „“、法语 «»、中文 “”），弯引号需转义（如 `\u201E...\u201C`）；禁止 XML 转义（写 `&` 不写 `&amp;`）。

## 排错

- 工具不出现：确认 `xcrun mcpbridge` 能独立运行（报 license 错误就先开一次 Xcode）。
- 第三方替代方案：npm 包 `xcodebuildmcp`（`npx xcodebuildmcp`），工具集与本仓库文档不一定一致，本仓库文档以官方 `xcrun mcpbridge` 为准。
