import datetime as dt

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)

    expences: Mapped['Expence'] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.first_name!r})'


class Item(Base):
    __tablename__ = 'items'
    name: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'Item(name={self.name!r})'


class Expence(Base):
    __tablename__ = 'expences'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item_name: Mapped[str] = mapped_column(ForeignKey('items.name'))
    price: Mapped[int] = mapped_column(Integer)
    cdate: Mapped[dt.datetime] = mapped_column(
            DateTime,
            default=dt.datetime.utcnow,
        )

    user: Mapped['User'] = relationship(back_populates='expences')
