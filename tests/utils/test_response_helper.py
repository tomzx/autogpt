from autogpt.utils.response_helper import extract_code


def test_extract_code():
    assert extract_code("Some text before\n```python\nprint('hello world')\n```\nSome text after") == (
        "print('hello world')",
        "python",
    )
    assert extract_code("Some text before\n```\nprint('hello world')\n```\nSome text after") == (
        "print('hello world')",
        None,
    )
