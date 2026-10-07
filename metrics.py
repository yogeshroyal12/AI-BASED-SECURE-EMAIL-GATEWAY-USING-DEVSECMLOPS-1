from prometheus_client import Counter, Histogram

REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
)

PREDICTIONS = Counter(
    "email_predictions_total",
    "Total email predictions",
    ["prediction"],
)

ACTIONS = Counter(
    "email_actions_total",
    "Total email security actions",
    ["action"],
)

SECURITY_BLOCKS = Counter(
    "security_blocks_total",
    "Runtime security blocks",
    ["reason"],
)

SECURITY_EVENTS = Counter(
    "security_events_total",
    "Security events",
    ["event_type"],
)
