import datetime as dt

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
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

    def __repr__(self) -> str:
        return f'Category(name={self.name!r})'


class Item(Base):
    __tablename__ = 'items'
    name: Mapped[str] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(ForeignKey('categories.name'))

    def __repr__(self) -> str:
        return f'Item(name={self.name!r})'

    __table_args__ = (
        UniqueConstraint('item_name', 'category_name'),
    )


class Expence(Base):
    __tablename__ = 'expences'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    category_name: Mapped[str] = mapped_column(ForeignKey('categories.name'))
    item_name: Mapped[str] = mapped_column(ForeignKey('items.name'))
    price: Mapped[int] = mapped_column(Integer)
    cdate: Mapped[dt.datetime] = mapped_column(
            DateTime,
            default=dt.datetime.now,
        )
