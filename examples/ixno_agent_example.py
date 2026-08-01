# ============================================================
# IXNO 云端基因池 — 其他 Agent 接入示例 (零依赖版)
# 让任何 AI Agent / 程序通过 HTTP 接入 ixno.com 基因池
# 用法: python3 ixno_agent_example.py
# ============================================================
import json
import urllib.request
import urllib.parse

BASE = "https://ixno.com/api/v1"   # 云端基因池 Base URL


def api(method: str, path: str, body: dict | None = None, key: str = "") -> dict:
    """通用 HTTP 请求封装（无第三方依赖，仅标准库）"""
    url = BASE + path
    data = json.dumps(body).encode() if body else None
    headers = {"Accept": "application/json"}
    if body:
        headers["Content-Type"] = "application/json"
    if key:
        headers["IXNO-API-Key"] = key          # 写操作需要 Key
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8", "replace")
        return json.loads(raw) if raw else {}


def main():
    print("=" * 50)
    print("IXNO Agent 接入演示")
    print("=" * 50)

    # 1) 健康检查 — Agent 接入的第一步：确认服务活着
    h = api("GET", "/health")
    print(f"\n[1] /health → {h}")

    # 2) 统计 — 了解基因池规模
    s = api("GET", "/stats")
    print(f"[2] /stats → 总基因: {s.get('total_genes')}, 领域数: {s.get('total_domains')}")

    # 3) 领域分布
    d = api("GET", "/domains")
    if isinstance(d, list) and d:
        top = [f"{x['domain']}={x['count']}" for x in d[:3]]
        print(f"[3] /domains → 前3领域: {top}")

    # 4) 拉基因（示例：取前2条）
    g = api("GET", "/genes?limit=2")
    genes = g.get("genes", [])
    print(f"[4] /genes → {len(genes)} 条样本")
    for x in genes[:1]:
        print(f"    基因: {x.get('gene_id', '')[:40]} | fitness={x.get('fitness')}")

    # 5) 注册 API Key（如需写权限；生产环境应缓存，勿每次调用）
    # key = api("POST", "/register", {"name": "my_agent"})
    # print(f"[5] /register → {key}")

    print("\n[OK] 接入成功！更多端点见 README「其他 Agent 接入」章节")


if __name__ == "__main__":
    main()
