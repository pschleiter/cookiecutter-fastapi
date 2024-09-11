from typing import TypeVar

from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from {{ cookiecutter.pkg_name }}.domain import model


class Base(DeclarativeBase):
    pass


ModelClass = TypeVar('ModelClass')
BaseClass = TypeVar('BaseClass')


def map_to_model(pydantic_class: type[ModelClass]):
    def wrapper(cls: type[BaseClass]):
        def to_pydantic(self: BaseClass) -> ModelClass:
            return pydantic_class.model_validate(obj=self, from_attributes=True)

        @classmethod
        def from_pydantic(cls: type[BaseClass], obj: ModelClass) -> BaseClass:
            return cls(**obj.model_dump())

        cls.to_pydantic = to_pydantic
        cls.from_pydantic = from_pydantic

        return cls

    return wrapper


@map_to_model(model.Dummy)
class DummyTable(Base):
    __tablename__ = 'dummy_table'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    nickname: Mapped[str | None]
