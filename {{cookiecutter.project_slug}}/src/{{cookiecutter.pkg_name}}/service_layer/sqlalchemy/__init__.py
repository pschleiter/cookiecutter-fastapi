import asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from {{ cookiecutter.pkg_name }}.adapters.sqlalchemy import repository as sql_repository
from {{ cookiecutter.pkg_name }}.service_layer.interface import AbstractUnitOfWork


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, db_uri: str):
        self.session_factory = async_sessionmaker(bind=create_async_engine(db_uri))

    async def __aenter__(self) -> AbstractUnitOfWork:
        self.session: AsyncSession = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=asyncio.current_task,
        )
        self.repository = sql_repository.SqlAlchemyRepository(session=self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)
        self.repository = None
        await self.session.close()

    async def _commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
