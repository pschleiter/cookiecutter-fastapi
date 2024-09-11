from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi_keycloak_middleware import setup_keycloak_middleware

from {{ cookiecutter.pkg_name }}.bootstrap import bootstrap
from {{ cookiecutter.pkg_name }}.config import Config
from {{ cookiecutter.pkg_name }}.entrypoints.state import State
from {{ cookiecutter.pkg_name }}.service_layer.interface import AbstractUnitOfWork


def create_api(
    uow: AbstractUnitOfWork | None = None, config: Config | None = None
) -> FastAPI:
    if config is None:
        config = Config()

    if uow is None:
        from {{ cookiecutter.pkg_name }}.service_layer.sqlalchemy import SqlAlchemyUnitOfWork  # PLC0415

        uow = SqlAlchemyUnitOfWork(
            db_uri=config.database_uri,
        )

    @asynccontextmanager
    async def lifespan(app: FastAPI):  # noqa ARG001
        yield State(service=await bootstrap(uow=uow), config=config)

    api = FastAPI(
        lifespan=lifespan,
        root_path=config.root_path,
    )

    setup_keycloak_middleware(
        app=api,
        keycloak_configuration=config.get_keycloak_config(),
    )
    api.add_middleware(SessionMiddleware, **config.get_session_arguments())
    api.add_middleware(CORSMiddleware, **config.get_cors_arguments())

    from {{ cookiecutter.pkg_name }}.entrypoints.router import dummy

    api.include_router(dummy.router, prefix='/dummy', tags=['test'])

    return api
