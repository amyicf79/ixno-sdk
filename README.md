# IXNO SDK (Python)

> Thin Python client for the **IXNO Cloud Gene Pool** — search, push, and register genes over REST. Zero third-party dependencies (stdlib only).
> IXNO 云端基因池的 Python 轻客户端——REST 搜索/推送/注册。零第三方依赖（仅标准库）。

## Install / 安装

```bash
pip install ixno-sdk
# or from source:
git clone https://github.com/your-org/ixno-sdk.git && cd ixno-sdk && pip install -e .
```

## Quickstart / 快速开始

```python
from ixno import IXNO

c = IXNO()                       # read-only, no key needed
print(c.health())                # {"status": "ok", "version": "8.2.0", ...}
print(c.search("中医", limit=5)) # Chinese search supported via keywords column
print(c.stats())

# write operations need an API key / 写操作需要 API Key
c2 = IXNO(api_key="ixno-xxxx")
c2.push("my_gene_001", "My Gene", "body content", domain="Custom", fitness=0.8)
```

## CLI

```bash
ixno health
ixno stats
ixno search "中医" --limit 5
ixno push --id g1 --name "demo" --body "hello" --key ixno-xxxx
```

## API Reference / 接口一览

| Method | Endpoint | Auth | Description / 说明 |
|---|---|---|---|
| `health()` | GET /api/v1/health | — | service status |
| `stats()` | GET /api/v1/stats | — | pool statistics |
| `search(q)` | GET /api/v1/search | — | keyword search (中文可用) |
| `get_gene(id)` | GET /api/v1/genes/{id} | — | single gene |
| `list_genes()` | GET /api/v1/genes | — | paged list |
| `domains()` | GET /api/v1/domains | — | domain distribution |
| `validate()` | POST /api/v1/validate | — | validate payload |
| `push(...)` | POST /api/v1/push | **key** | async push |
| `delete(id)` | DELETE /api/v1/genes/{id} | **key** | delete gene |
| `register(name)` | POST /api/v1/register | — | get a new key (10min/IP) |
| `usage()` | GET /api/v1/usage | **key** | key identity |

## Get an API Key / 获取 API Key

```python
from ixno import IXNO
key = IXNO().register("my_username")   # returns {"api_key": "ixno-..."}
```
Note: only the write endpoints (push/delete) need a key. Search and reads are open. / 仅写端点（push/delete）需要 Key，搜索与读取开放。

## License / 许可

MIT
