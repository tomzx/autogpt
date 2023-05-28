from autogpt.configuration.configuration import Configuration


def is_debug() -> bool:
    return Configuration.debug


def is_profiling() -> bool:
    return Configuration.profile
