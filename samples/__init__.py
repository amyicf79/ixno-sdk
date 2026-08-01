# Public sample genes for IXNO SDK demo / 用于 SDK 演示的公开样本基因
# These are NOT from the private pool — free to embed in docs & tests.
# 非私有基因池数据，可自由嵌入文档与测试。

SAMPLE_GENES = [
    {
        "gene_id": "sample_hello_world",
        "name": "Hello World Agent",
        "body": "A minimal agent that greets the user. Demonstrates the gene format.",
        "domain": "Sample",
        "fitness": 0.9,
        "tags": "sample,demo,hello",
    },
    {
        "gene_id": "sample_retry_wrapper",
        "name": "Retry Wrapper",
        "body": "Wraps a function call with exponential backoff retry on transient errors.",
        "domain": "Sample",
        "fitness": 0.85,
        "tags": "sample,retry,robustness",
    },
    {
        "gene_id": "sample_timeout_guard",
        "name": "Timeout Guard",
        "body": "Enforces a maximum execution time for a wrapped function using signals.",
        "domain": "Sample",
        "fitness": 0.8,
        "tags": "sample,timeout,safety",
    },
]
