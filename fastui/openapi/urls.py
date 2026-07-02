from __future__ import annotations


def build_docs_urls(
    *,
    docs_url: str = "/docs",
    openapi_url: str = "/openapi.json",
) -> dict[str, str]:
    """Build documentation URLs with an optional shared prefix.

    Args:
        docs_url: URL path for the Swagger UI page.
        openapi_url: URL path for the OpenAPI JSON schema.

    Returns:
        Dictionary with ``docs_url`` and ``openapi_url`` keys.
    """
    return {
        "docs_url": docs_url,
        "openapi_url": openapi_url,
    }
