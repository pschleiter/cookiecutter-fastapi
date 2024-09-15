import asyncio

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from {{ cookiecutter.pkg_name }}.adapters.sqlmodel import repository as sql_repository
from {{ cookiecutter.pkg_name }}.service_layer.interface import AbstractUnitOfWork


class SqlModelUnitOfWork(AbstractUnitOfWork):
    def __init__(self, db_uri: str):
        self.session_factory = async_scoped_session(
            session_factory=async_sessionmaker(
                bind=create_async_engine(db_uri), class_=AsyncSession
            ),
            scopefunc=asyncio.current_task,
        )

    async def __aenter__(self) -> AbstractUnitOfWork:
        self.session: AsyncSession = self.session_factory()
        self.repository = sql_repository.SqlModelRepository(session=self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)
        self.repository = None
        await self.session.close()

    async def _commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
