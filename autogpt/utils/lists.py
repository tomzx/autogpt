import re
from typing import List


def contains_list(text: str) -> bool:
    """Check if a text contains a list.
    Supported formats: prefixed by a dash or a star.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if the text contains a list, False otherwise.
    """
    return count_list_items(text) > 0


def count_list_items(text: str) -> int:
    """Count the number of items in a list.
    Supported formats: prefixed by a dash or a star.

    Args:
        text (str): The text to count the number of items in the list.

    Returns:
        int: The number of items in the list.
    """
    return sum(re.match(r"^(\d+\.|-|\*)", line) is not None for line in text.splitlines())


def extract_list(text: str) -> List[str]:
    """Extract a list from a text.
    Supported formats: prefixed by a dash or a star or a number.

    Args:
        text (str): The text to extract the list from.

    Returns:
        List[str]: The list of strings extracted from the text.
    """
    lines = text.splitlines()
    result = []
    for line in lines:
        match = re.match(r"^(\d+\.|-|\*)", line)
        if match:
            result += [line[match.end() :].strip()]
    return result
