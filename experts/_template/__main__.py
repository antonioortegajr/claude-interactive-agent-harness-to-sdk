"""Callable entrypoint: ``python -m experts._template ask "<question>"``."""

from harness.cli import main

if __name__ == "__main__":
    raise SystemExit(main("experts._template"))
