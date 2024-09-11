from pydantic import BaseModel


class Dummy(BaseModel):
    id: int
    name: str
    nickname: str | None = None
