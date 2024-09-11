import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def init_repository(self):
        raise NotImplementedError
