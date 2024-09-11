import abc

from {{ cookiecutter.pkg_name }}.adapters.interface import repository


class AbstractUnitOfWork(abc.ABC):
    repository: repository.AbstractRepository

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        self._commit()

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

    async def init_repository(self):
        async with self as uow:
            await uow.repository.init_repository()
