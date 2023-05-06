from typing import Optional


class Request:
    prompt: str
    # TODO(tom@tomrochette.com): Find a way to move this out of this class
    notion_interaction_id: Optional[str]

    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
        self.notion_interaction_id = None
