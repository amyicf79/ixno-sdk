"""ixno CLI — quick gene pool access from the terminal."""
import argparse
import json
import sys

from .client import IXNO, IXNOError, DEFAULT_ENDPOINT


def main(argv=None):
    p = argparse.ArgumentParser(prog="ixno", description="IXNO gene pool CLI")
    p.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="API base URL")
    p.add_argument("--key", default="", help="API key (write ops)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("health", help="service status")
    sp = sub.add_parser("stats", help="pool stats")
    sp = sub.add_parser("search", help="search genes")
    sp.add_argument("q", help="query (Chinese OK)")
    sp.add_argument("--limit", type=int, default=10)
    sp = sub.add_parser("push", help="push a gene (needs key)")
    sp.add_argument("--id", required=True)
    sp.add_argument("--name", required=True)
    sp.add_argument("--body", required=True)
    sp.add_argument("--domain", default="External")
    sp.add_argument("--fitness", type=float, default=0.5)

    args = p.parse_args(argv)
    c = IXNO(api_key=args.key, endpoint=args.endpoint)
    try:
        if args.cmd == "health":
            out = c.health()
        elif args.cmd == "stats":
            out = c.stats()
        elif args.cmd == "search":
            out = c.search(args.q, limit=args.limit)
        elif args.cmd == "push":
            out = c.push(args.id, args.name, args.body,
                         domain=args.domain, fitness=args.fitness)
        else:
            p.error("unknown command")
        print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    except IXNOError as e:
        print(f"ixno: error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
