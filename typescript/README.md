# IXNO SDK (TypeScript)

> Thin TypeScript client for the **IXNO Cloud Gene Pool** — search, push, register genes over REST. Zero runtime dependencies (native `fetch`).
> IXNO 云端基因池的 TypeScript 客户端——REST 搜索/推送/注册。零运行时依赖（原生 fetch）。

## Install / 安装

```bash
npm install ixno-sdk-ts
# or from source:
git clone https://github.com/your-org/ixno-sdk-ts.git && cd ixno-sdk-ts
npm install && npm run build
```

## Quickstart / 快速开始

```typescript
import { IXNO } from "ixno-sdk-ts";

const c = new IXNO();                       // read-only, no key needed
const health = await c.health();            // { status: "ok", version: "8.2.0", ... }
const res = await c.search("中医", 5);      // Chinese search via keywords column
console.log(health, res.total);

// write operations need an API key / 写操作需要 API Key
const c2 = new IXNO({ apiKey: "ixno-xxxx" });
await c2.push({ gene_id: "g1", name: "demo", body: "hello", fitness: 0.8 });
```

## API / 接口

| Method | Auth | Description / 说明 |
|---|---|---|
| `health()` | — | service status |
| `stats()` | — | pool statistics |
| `search(q, limit, domain)` | — | keyword search (中文可用) |
| `getGene(id)` | — | single gene |
| `listGenes()` | — | paged list |
| `domains()` | — | domain distribution |
| `push(gene)` | **key** | async push |
| `delete(id)` | **key** | delete gene |
| `register(name)` | — | get a new key (10min/IP) |
| `usage()` | **key** | key identity |

## License / 许可

MIT
