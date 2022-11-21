from dataclasses import dataclass
import json
from typing import Optional


@dataclass
class Message:
    video_fid: str
    username: str
    email: str
    mp3_fid: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        return Message(
            video_fid=data.get("video_fid"),
            username=data.get("username"),
            mp3_fid=data.get("mp3_fid"),
            email=data.get("email"),
        )

    def to_dict(self) -> dict:
        return {
            "video_fid": self.video_fid,
            "username": self.username,
            "mp3_fid": self.mp3_fid,
            "email": self.email,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
