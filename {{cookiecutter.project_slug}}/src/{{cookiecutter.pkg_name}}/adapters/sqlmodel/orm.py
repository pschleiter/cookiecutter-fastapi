from sqlalchemy import BigInteger
from sqlmodel import SQLModel, Field

from {{ cookiecutter.pkg_name }}.domain import model

metadata = SQLModel.metadata


class DummyTable(model.Dummy, table=True):
    __tablename__ = 'dummy_table'

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
