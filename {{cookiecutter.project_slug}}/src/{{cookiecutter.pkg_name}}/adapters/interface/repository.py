import abc

from {{ cookiecutter.pkg_name }}.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def init_repository(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def create_dummy(self, dummy: model.Dummy):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_dummy(self, name: str):
        raise NotImplementedError
