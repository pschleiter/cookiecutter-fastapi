from {{ cookiecutter.pkg_name }}.domain import model
from {{ cookiecutter.pkg_name }}.service_layer.interface import AbstractUnitOfWork


class Service:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create_dummy(self, dummy: model.Dummy):
        async with self.uow as uow:
            await uow.repository.create_dummy(dummy=dummy)
            await uow.commit()

    async def get_nickname(self, name: str) -> str:
        async with self.uow as uow:
            dummy = await uow.repository.get_dummy(name=name)
            return dummy.nickname or dummy.name
