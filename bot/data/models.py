import datetime as dt
from typing import List

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


meta = MetaData(naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_`%(constraint_name)s`',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s'
      })


class Base(DeclarativeBase):
    metadata = meta


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=True)

    expenses: Mapped[List['Expense']] = relationship(back_populates='user')
    items: Mapped[List['Item']] = relationship(back_populates='user')
    group: Mapped['Group'] = relationship(back_populates='users')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.first_name!r})'


class Item(Base):
    __tablename__ = 'items'
    name: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='items')

    def __repr__(self) -> str:
        return f'Item(name={self.name!r})'


class Expense(Base):
    __tablename__ = 'expenses'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item_name: Mapped[str] = mapped_column(ForeignKey('items.name'))
    price: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=True)
    cdate: Mapped[dt.datetime] = mapped_column(
            DateTime,
            default=dt.datetime.utcnow,
        )
    cdate_tz: Mapped[dt.datetime] = mapped_column(
            DateTime,
            default=dt.datetime.utcnow,
            nullable=True,
        )
    is_replenishment: Mapped[bool] = mapped_column(
            Boolean,
            default=False,
            nullable=True,
        )

    user: Mapped['User'] = relationship(back_populates='expenses')


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cdate: Mapped[dt.datetime] = mapped_column(
            DateTime,
            default=dt.datetime.utcnow,
        )

    users: Mapped[List['User']] = relationship(back_populates='group')


class Release(Base):
    __tablename__ = 'releases'
    id: Mapped[str] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String, nullable=False)
    is_broadcasted: Mapped[bool] = mapped_column(Boolean, default=False)
