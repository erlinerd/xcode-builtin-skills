---
name: ask-xcode
description: >-
  路由到 10 个 Xcode 内建技能的入口：String Catalog 翻译对（translation / translation-coordinator）与 8 个 Apple 专家技能（SwiftUI、App Intents、bounds-safety、安全加固、文档型应用、UIKit 现代化）。用户提到翻译 String Catalog / 本地化 Xcode 项目、SwiftUI 最佳实践或 27 新特性、App Intents 及其 27 更新、C 代码采用 -fbounds-safety、Xcode 安全加固审计、文档型 SwiftUI 应用、UIKit 多窗口现代化，或问"该用哪个 Xcode 技能"时使用——即使没点名技能名。Route requests to the 10 built-in Xcode skills; use whenever a task matches one of their trigger domains or the user asks which Xcode skill applies.
---

# ask-xcode — Xcode 内建技能路由

按请求特征选中目标技能后，加载该技能并按其指引执行。本技能只路由，不干活。

## 路由表

| 请求特征 | 目标技能 | 依赖 |
|---|---|---|
| 翻译一小批 String Catalog 字符串（已给定 key 和语言） | `translation` | Xcode MCP |
| 整项目加语言、批量翻译、翻译编排与验证 | `translation-coordinator` | Xcode MCP |
| 写/改 SwiftUI 代码，问最佳实践、性能、动画、@Observable、ForEach、List、本地化 | `swiftui-specialist` | 无 |
| SwiftUI 27 新 API、@State 宏报错、SDK 升级适配 | `swiftui-whats-new-27` | 无 |
| 写/改/评审 App Intents 代码 | `app-intents-specialist` | 无 |
| App Intents 27 新 API、迁移、弃用清单 | `app-intents-whats-new-27` | 无 |
| C 代码采用或排查 `-fbounds-safety`（`__counted_by` 等注解） | `adopt-c-bounds-safety` | 无 |
| Xcode 工程安全加固：编译警告、静态分析、Enhanced Security | `audit-xcode-security-settings` | 无 |
| 文档型 SwiftUI 应用（Document 协议、DocumentGroup、UTType、迁移） | `building-document-based-swiftui-applications` | 无 |
| UIKit 多窗口现代化（mainScreen、safe area、生命周期 API 迁移） | `uikit-app-modernization` | 无 |

## 规则

1. 一次请求命中多个技能：按主意图选主技能先加载，其余在执行到相关部分时再加载。
2. 翻译二选一：只给了一批 key → `translation`；整项目/加新语言/要编排 → `translation-coordinator`（它会自己派发 translation 子代理）。
3. 调 StringCatalog 工具前的激活规则是工具强制要求，路由后不得省略。
4. 未命中上表的 Xcode 问题（构建、签名、模拟器、General 设置）不路由，按常规处理。
