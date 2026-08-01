"""IXNO Cloud Gene Pool — thin client.

Talk to the IXNO cloud gene pool over REST.
基因池云端 API 的轻量客户端。

Usage / 用法:
    from ixno import IXNO
    c = IXNO(api_key="...")   # only needed for push/delete
    c.health()
    c.search("中医")
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

__all__ = ["IXNO", "IXNOError"]

DEFAULT_ENDPOINT = "https://ixno.com/api/v1"


class IXNOError(Exception):
    """Raised on API-level errors / API 层错误时抛出。"""


class IXNO:
    """IXNO cloud gene pool client. 无第三方依赖（仅标准库 urllib）。"""

    def __init__(self, api_key: str = "", endpoint: str = DEFAULT_ENDPOINT,
                 timeout: float = 20.0):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")
        self.timeout = timeout

    # ---------- low-level ----------
    def _request(self, method: str, path: str, body: Optional[dict] = None,
                 auth: bool = False) -> Dict[str, Any]:
        url = f"{self.endpoint}{path}"
        data = None
        headers = {"Accept": "application/json"}
        if body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        if auth:
            if not self.api_key:
                raise IXNOError("api_key required for this operation / 该操作需要 api_key")
            headers["IXNO-API-Key"] = self.api_key
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8", "replace")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            raise IXNOError(f"HTTP {e.code}: {detail}") from e
        except urllib.error.URLError as e:
            raise IXNOError(f"network error / 网络错误: {e.reason}") from e

    # ---------- read endpoints (no auth) ----------
    def health(self) -> Dict[str, Any]:
        """Service health & version / 服务健康与版本."""
        return self._request("GET", "/health")

    def search(self, q: str, domain: str = "", limit: int = 20,
               sort: str = "") -> Dict[str, Any]:
        """Search the gene pool. Supports Chinese via keywords column.
        搜索基因池（中文通过 keywords 列支持）。"""
        params = {"q": q, "limit": limit}
        if domain: params["domain"] = domain
        if sort: params["sort"] = sort
        qs = urllib.parse.urlencode(params)
        return self._request("GET", f"/search?{qs}")

    def get_gene(self, gene_id: str) -> Dict[str, Any]:
        """Fetch a single gene by id / 按 id 获取单个基因."""
        return self._request("GET", f"/genes/{urllib.parse.quote(gene_id)}")

    def domains(self) -> List[Dict[str, Any]]:
        """List domains with counts / 列出域与统计."""
        return self._request("GET", "/domains")

    def stats(self) -> Dict[str, Any]:
        """Pool statistics / 基因池统计."""
        return self._request("GET", "/stats")

    def list_genes(self, domain: str = "", limit: int = 100,
                   offset: int = 0) -> Dict[str, Any]:
        """List genes (paged) / 分页列出基因."""
        qs = urllib.parse.urlencode({"domain": domain, "limit": limit, "offset": offset})
        return self._request("GET", f"/genes?{qs}")

    def validate(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a gene payload without persisting / 校验基因但不落库."""
        return self._request("POST", "/validate", body=body)

    # ---------- write endpoints (need api_key) ----------
    def push(self, gene_id: str, name: str, body: str, domain: str = "External",
             fitness: float = 0.5, tags: str = "", **extra) -> Dict[str, Any]:
        """Push a gene into the pool (async, returns queued).
        推送基因入池（异步，返回 queued）。"""
        payload = {
            "gene_id": gene_id, "name": name, "body": body,
            "domain": domain, "fitness": fitness, "tags": tags,
            **extra,
        }
        return self._request("POST", "/push", body=payload, auth=True)

    def delete(self, gene_id: str) -> Dict[str, Any]:
        """Delete a gene / 删除基因."""
        return self._request("DELETE", f"/genes/{urllib.parse.quote(gene_id)}", auth=True)

    def register(self, name: str) -> Dict[str, Any]:
        """Register a new API key (10 min/IP anti-abuse).
        注册新 API Key（每 IP 10 分钟一次）。"""
        return self._request("POST", "/register", body={"name": name})

    def usage(self) -> Dict[str, Any]:
        """Identity info of the current key / 当前 key 的身份信息."""
        return self._request("GET", "/usage", auth=True)
