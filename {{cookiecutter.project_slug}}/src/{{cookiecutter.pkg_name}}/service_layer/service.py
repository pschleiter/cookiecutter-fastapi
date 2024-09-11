from {{ cookiecutter.pkg_name }}.service_layer.interface import AbstractUnitOfWork


class Service:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
