def server_main() -> None:
    from .mcp import server

    """Main entry point for MCP server."""
    server.main()


def api_main() -> None:
    from . import start

    """Main entry point for API server."""
    start.main()


# Optionally expose other important items at package level
__all__ = ["server_main", "api_main"]
