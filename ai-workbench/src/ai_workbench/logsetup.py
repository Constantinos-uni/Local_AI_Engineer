import logging

from rich.logging import RichHandler

def setup_logging(level: str = "INFO") -> None:
    """Route logging through rich so logs are readable *and* structured."""
    logging.basicConfig(
        level=level,
        format="%(name)s: %(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
        force=True,
    )
