MIME_JSON = "application/json"
MIME_PROBLEM_JSON = "application/problem+json"
MIME_HTML = "text/html"
MIME_ANY = "*/*"
MIME_XML = "application/xml"
MIME_YAML = "application/yaml"

JSON_CONTENT_TYPES = frozenset(
    [
        "application/json",
        "application/problem+json",
        "application/vnd.api+json",
        "application/hal+json",
        "application/ld+json",
    ]
)

HTML_CONTENT_TYPES = frozenset(
    [
        "text/html",
        "application/xhtml+xml",
    ]
)
