from {{ cookiecutter.pkg_name }}.service_layer.interface import AbstractUnitOfWork
from {{ cookiecutter.pkg_name }}.service_layer.service import Service


async def bootstrap(uow: AbstractUnitOfWork) -> Service:
    await uow.init_repository()

    return Service(uow=uow)
