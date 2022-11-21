from dataclasses import dataclass


@dataclass
class Message:
    video_fid: str
    username: str
    email: str
    mp3_fid: str

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        if not data.get("mp3_fid"):
            raise ValueError("mp3_fid is required")
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

    def mp3_url(self, base_endpoint: str):
        return f"{base_endpoint}/{self.mp3_fid}"
