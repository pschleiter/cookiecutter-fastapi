from typing import TypedDict

from {{ cookiecutter.pkg_name }}.config import Config
from {{ cookiecutter.pkg_name }}.service_layer.service import Service


class State(TypedDict):
    service: Service
    config: Config
