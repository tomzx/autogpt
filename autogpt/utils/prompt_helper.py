import json
import textwrap
from typing import Any, Dict, Optional

import yaml


def return_json(output: Optional[Dict[str, Any]] = None) -> str:
    prompt = "Return your response in JSON format."
    if output is not None:
        prompt += " Use the following format for your output:\n"
        prompt += json.dumps(output)
    return prompt


def return_yaml(output: Optional[Dict[str, Any]] = None, default_flow_style: bool = False) -> str:
    prompt = "Return your response in YAML format."
    if output is not None:
        prompt += " Use the following format for your output:\n"
        prompt += yaml.dump(output, default_flow_style=default_flow_style).strip()
    return prompt
