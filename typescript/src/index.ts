/**
 * IXNO Cloud Gene Pool — TypeScript client.
 * 基因池云端 API 的 TypeScript 客户端。零依赖（仅原生 fetch）。
 */

export const DEFAULT_ENDPOINT = "https://ixno.com/api/v1";

export class IXNOError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "IXNOError";
  }
}

export interface IXNOOptions {
  apiKey?: string;
  endpoint?: string;
  timeoutMs?: number;
}

export interface Gene {
  gene_id: string;
  name: string;
  fitness: number;
  domain: string;
  [k: string]: unknown;
}

export interface SearchResult {
  query: string;
  total: number;
  results: Gene[];
}

export class IXNO {
  private apiKey: string;
  private endpoint: string;
  private timeoutMs: number;

  constructor(opts: IXNOOptions = {}) {
    this.apiKey = opts.apiKey ?? "";
    this.endpoint = (opts.endpoint ?? DEFAULT_ENDPOINT).replace(/\/$/, "");
    this.timeoutMs = opts.timeoutMs ?? 20_000;
  }

  private async request<T = unknown>(
    method: string,
    path: string,
    body?: unknown,
    auth = false,
  ): Promise<T> {
    const url = `${this.endpoint}${path}`;
    const headers: Record<string, string> = { Accept: "application/json" };
    let payload: string | undefined;
    if (body !== undefined) {
      payload = JSON.stringify(body);
      headers["Content-Type"] = "application/json";
    }
    if (auth) {
      if (!this.apiKey) {
        throw new IXNOError("api_key required for this operation / 该操作需要 api_key");
      }
      headers["IXNO-API-Key"] = this.apiKey;
    }
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), this.timeoutMs);
    try {
      const res = await fetch(url, {
        method,
        headers,
        body: payload,
        signal: ctrl.signal,
      });
      const text = await res.text();
      if (!res.ok) {
        throw new IXNOError(`HTTP ${res.status}: ${text.slice(0, 300)}`, res.status);
      }
      return text ? (JSON.parse(text) as T) : ({} as T);
    } finally {
      clearTimeout(timer);
    }
  }

  // ---------- read (no auth) ----------
  health(): Promise<Record<string, unknown>> {
    return this.request("/health");
  }

  search(q: string, limit = 20, domain = ""): Promise<SearchResult> {
    const params = new URLSearchParams({ q, limit: String(limit) });
    if (domain) params.set("domain", domain);
    return this.request(`/search?${params.toString()}`);
  }

  getGene(geneId: string): Promise<Gene> {
    return this.request(`/genes/${encodeURIComponent(geneId)}`);
  }

  stats(): Promise<Record<string, unknown>> {
    return this.request("/stats");
  }

  domains(): Promise<Array<Record<string, unknown>>> {
    return this.request("/domains");
  }

  listGenes(domain = "", limit = 100, offset = 0): Promise<Record<string, unknown>> {
    const params = new URLSearchParams({ domain, limit: String(limit), offset: String(offset) });
    return this.request(`/genes?${params.toString()}`);
  }

  // ---------- write (need apiKey) ----------
  push(gene: Gene): Promise<Record<string, unknown>> {
    return this.request("/push", gene, true);
  }

  delete(geneId: string): Promise<Record<string, unknown>> {
    return this.request(`/genes/${encodeURIComponent(geneId)}`, undefined, true);
  }

  register(name: string): Promise<Record<string, unknown>> {
    return this.request("/register", { name });
  }

  usage(): Promise<Record<string, unknown>> {
    return this.request("/usage", undefined, true);
  }
}

export default IXNO;
