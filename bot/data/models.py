from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.first_name!r})'


class Category(Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(primary_key=True)

    items: Mapped[List['Item']] = relationship(
            back_populates='category',
        )

    def __repr__(self) -> str:
        return f'Category(name={self.name!r})'


class Item(Base):
    __tablename__ = 'items'
    name: Mapped[str] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(ForeignKey('categories.name'))

    category: Mapped['Category'] = relationship(
            back_populates='items',
        )

    def __repr__(self) -> str:
        return f'Item(name={self.name!r})'
