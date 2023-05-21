from typing import Optional

from autogpt.session.session import Session


class Request:
    task: str
    prompt: str
    # TODO(tom@tomrochette.com): Find a way to move this out of this class
    notion_interaction_id: Optional[str]
    session: Optional[Session]

    def __init__(self, prompt: str, task: str) -> None:
        self.prompt = prompt
        self.task = task
        self.notion_interaction_id = None
        self.session = None
