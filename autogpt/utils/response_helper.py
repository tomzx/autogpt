from typing import Optional, Tuple


def extract_code(text: str) -> Tuple[str, Optional[str]]:
    if "```" not in text:
        raise ValueError("Text does not contain a code block.")

    code_block = text.split("```")[1]
    code_lines = code_block.split("\n")
    language = code_lines[0].strip() or None
    code = "\n".join(code_lines[1:]).strip()

    return code, language
