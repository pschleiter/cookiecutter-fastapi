from sqlmodel import SQLModel


class Dummy(SQLModel):
    name: str
    nickname: str | None = None
