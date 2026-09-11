"""Explicit single-provider OpenRouter routing, shared by smoke and main runs."""
from urllib.parse import urlsplit


def routing_settings(args):
    slug = getattr(args, "openrouter_provider", None)
    name = getattr(args, "openrouter_provider_name", None)
    url = urlsplit(args.base_url)
    is_openrouter = url.hostname == "openrouter.ai"
    if not is_openrouter and not slug and not name:
        return None
    if (not is_openrouter or url.scheme != "https" or url.path.rstrip("/") != "/api/v1"
            or not slug or not slug.strip() or not name or not name.strip()):
        raise ValueError("OpenRouter requires its HTTPS API base, one provider slug, and exact provider response name")
    return {
        "provider_preferences": {
            "only": [slug], "order": [slug],
            "allow_fallbacks": False, "require_parameters": True,
        },
        "expected_provider_name": name,
    }


def add_routing_settings(settings, args):
    routing = routing_settings(args)
    if routing is not None:
        settings["openrouter_routing"] = routing
    return settings


def add_routing_arguments(parser):
    parser.add_argument("--openrouter-provider", help="Exact OpenRouter provider endpoint slug; disables fallbacks")
    parser.add_argument("--openrouter-provider-name", help="Exact expected provider name in every completion response")
