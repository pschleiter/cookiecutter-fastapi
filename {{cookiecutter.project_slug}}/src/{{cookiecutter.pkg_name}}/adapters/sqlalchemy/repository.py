from sqlalchemy.ext.asyncio import async_scoped_session

from {{ cookiecutter.pkg_name }}.adapters.interface.repository import AbstractRepository
from {{ cookiecutter.pkg_name }}.adapters.sqlalchemy import orm


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: async_scoped_session):
        self.session: async_scoped_session = session

    async def init_repository(self):
        async with self.session.bind.begin() as connection:
            await connection.run_sync(orm.Base.metadata.create_all)
