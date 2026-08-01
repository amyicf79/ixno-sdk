#!/usr/bin/env python3
"""Quickstart — run the demo end-to-end. / 端到端演示。

Run locally without cloud:  python examples/quickstart.py --offline
Run against cloud:        python examples/quickstart.py --key YOUR_KEY
"""
import argparse
import json
import sys

sys.path.insert(0, ".")

from samples import SAMPLE_GENES          # noqa: E402
from ixno import IXNO                     # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="demo with samples only")
    ap.add_argument("--key", default="", help="API key for push demo")
    args = ap.parse_args()

    c = IXNO(api_key=args.key)

    if args.offline:
        print("=== OFFLINE DEMO (samples only, no cloud) ===")
        for g in SAMPLE_GENES:
            print(f"  {g['gene_id']:24s} {g['name']}  fitness={g['fitness']}")
        print("\nOffline demo done. Add --key to talk to the real pool.")
        return 0

    print("=== 1. health ===")
    print(json.dumps(c.health(), ensure_ascii=False))

    print("\n=== 2. stats ===")
    try:
        print(json.dumps(c.stats(), ensure_ascii=False)[:300])
    except Exception as e:
        print("  (stats unavailable:", e, ")")

    print("\n=== 3. search '中医' (Chinese via keywords column) ===")
    r = c.search("中医", limit=3)
    print(f"  total={r.get('total')}")

    print("\n=== 4. push demo (needs key) ===")
    if args.key:
        g = SAMPLE_GENES[0]
        out = c.push(g["gene_id"], g["name"], g["body"],
                     domain=g["domain"], fitness=g["fitness"], tags=g["tags"])
        print(f"  push → {out}")
    else:
        print("  skipped (no --key)")

    print("\nDone. / 完成。")


if __name__ == "__main__":
    main()
