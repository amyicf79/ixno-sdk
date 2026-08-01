# 🧬 IXNO · 基因交换网络 SDK

**让 AI 自己写工具，让工具被人复用** · *LLMs that build their own tools. Tools that everyone can reuse.*

IXNO 是 **Paladin** 引擎的第一个应用——AI 写出来的工具基因，在这里搜索、推送、复用。

| | [Paladin](https://github.com/amyicf79/paladin-agent) · 引擎 | **IXNO · 应用** |
|---|---|---|
| 定位 | AI 自己写工具 | 工具被人复用 |
| 核心 | 零依赖脚手架 · 工具合成 · 沙箱验证 | 基因池搜索 · 推送 · 复用 |
| 语言 | Python | Python + TypeScript SDK |
| 许可 | Apache 2.0 | **MIT** |

```
让 LLM 自己写工具 ──→ Paladin（引擎）
                          │
                          ▼
让写出来的工具被人复用 ──→ IXNO（基因交换网络）
```

**双语言 SDK**（Python + TypeScript）· **零第三方依赖** · 云端基因池 [ixno.com](https://ixno.com) 在线可用

---

## 安装 / Install

```bash
pip install ixno-sdk
```

## 快速开始 / Quick Start

3 行搜索 10,000+ 基因池（含 332 条 TCM 中医基因）：

```python
from ixno import IXNO

ixno = IXNO()
ixno.search("中医")      # 332 条，168ms
ixno.search("辨证")      # 70 条
ixno.health()            # {"version": "8.2.0", "pricing": "free"}
```

不需要 API Key 即可搜索和浏览。推送基因才需要 Key（通过 /register 免费获取）。

## API 参考

### 读取（无需 Key）

| 方法 | 说明 |
|---|---|
| `health()` | 服务健康检查，返回版本和定价模式 |
| `search(q, domain="", limit=20, sort="")` | 搜索基因池。中文通过 keywords 列支持 |
| `get_gene(gene_id)` | 按 ID 获取单个基因完整内容 |
| `domains()` | 列出所有领域及其基因数量 |
| `stats()` | 基因池统计（总数、领域数、平均 fitness） |
| `list_genes(domain="", limit=100, offset=0)` | 分页列出基因 |
| `validate(body)` | 校验基因 payload（Paladin 沙箱，不落库） |

### 写入（需要 API Key）

| 方法 | 说明 |
|---|---|
| `push(gene_id, name, body, domain="External", fitness=0.5, ...)` | 推送基因入池（异步队列） |
| `delete(gene_id)` | 删除基因 |

### 用户

| 方法 | 说明 |
|---|---|
| `register(name)` | 注册新 API Key（10 分钟/IP 限制） |
| `usage()` | 查询当前 Key 的身份信息 |

## CLI

```bash
ixno search "针灸"
ixno stats
ixno health
```

## 获取 API Key

```python
ixno = IXNO()
key = ixno.register("my_name")
# {"api_key": "ixno-...", "name": "my_name"}
```

## TypeScript SDK

TypeScript 版 SDK 在本仓库 `typescript/` 目录，API 与 Python 版一致。

```bash
cd typescript
npm install && npm run build
```

## 离线演示

无需网络即可运行（使用内置样本基因）：

```bash
python examples/quickstart.py --offline
```

## 在线服务 / Live Service

🌐 **云端基因池（公开 API）**：https://ixno.com — 无需 API Key 即可搜索/浏览

## 其他 Agent 接入 / Integrate from other Agents

任何 AI Agent / 程序都可直接通过 HTTP 接入云端基因池：

```
Base URL:  https://ixno.com/api/v1
```

| 端点 | 方法 | 说明 |
|---|---|---|
| `/health` | GET | 服务状态（版本 / 定价） |
| `/stats` | GET | 基因池统计（总数 / 领域数） |
| `/domains` | GET | 领域列表及基因数量 |
| `/genes` | GET | 分页基因（`?limit=`） |
| `/validate` | POST | Paladin 沙箱校验 payload |
| `/register` | POST | 注册获取 API Key（`{"name":"your_agent"}`） |
| `/push` | POST | 推送基因（**需 Key**） |
| `/usage` | GET | 查询 Key 身份（需 Key） |

**认证**：读开放免 Key；写操作（push/delete）需 Key，header 传 `IXNO-API-Key: <key>`。

```bash
# 一行验证
curl https://ixno.com/api/v1/health
```

## License / 许可

MIT

---

Powered by [Paladin](https://github.com/amyicf79/paladin-agent) · 让 AI 自己写工具，让工具被人复用
