from typing import TYPE_CHECKING

from sqlmodel import select


if TYPE_CHECKING:
    from sqlmodel.ext.asyncio.session import Session

from {{ cookiecutter.pkg_name }}.domain import model
from {{ cookiecutter.pkg_name }}.adapters.interface.repository import AbstractRepository
from {{ cookiecutter.pkg_name }}.adapters.sqlmodel import orm


class SqlModelRepository(AbstractRepository):
    def __init__(self, session):
        self.session: Session = session

    async def init_repository(self):
        async with self.session.bind.begin() as connection:
            await connection.run_sync(orm.metadata.create_all)

    async def create_dummy(self, dummy: model.Dummy):
        self.session.add(orm.DummyTable.model_validate(dummy))

    async def get_dummy(self, name: str) -> model.Dummy | None:
        return (
            await self.session.exec(
                select(orm.DummyTable).where(orm.DummyTable.name == name)
            )
        ).first()
