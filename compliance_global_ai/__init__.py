def main() -> None:
    from . import server
    """Main entry point for the package."""
    server.main()


# Optionally expose other important items at package level
__all__ = ["main", "server"]
