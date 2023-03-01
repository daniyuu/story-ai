from typing import Dict

from shortuuid import uuid


class Story:
    def __init__(self, beginning: str):
        self.id: str = uuid()
        self.created_at = ''
        self.beginning: str = beginning
        self.content = ""

    def __repr__(self):
        return self.content

    def dump(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "content": self.content
        }
