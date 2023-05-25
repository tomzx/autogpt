import os


def is_debug() -> bool:
    return os.environ.get("DEBUG") == "1"


def is_profiling() -> bool:
    return os.environ.get("PROFILE") == "1"
