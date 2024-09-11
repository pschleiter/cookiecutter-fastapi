from typing import Annotated

from fastapi import Depends, Request

from {{ cookiecutter.pkg_name }}.service_layer.service import Service


def get_service(request: Request) -> Service:
    return request.state.service


ServiceDep = Annotated[Service, Depends(get_service)]
