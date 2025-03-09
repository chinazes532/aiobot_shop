import psycopg2

from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, String, BigInteger, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=False)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str]
    ref_link: Mapped[str]
    invited_by: Mapped[int] = mapped_column(BigInteger,
                                            nullable=True)
    ref_count: Mapped[int]
    balance: Mapped[int]
    date: Mapped[str]


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(55))


class Product(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(55))
    description: Mapped[str] = mapped_column(String(599))
    price: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))


class Percent(Base):
    __tablename__ = "percents"

    id: Mapped[intpk]
    count: Mapped[int]


class PromoCode(Base):
    __tablename__ = "promocodes"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(55))
    percent: Mapped[int]
    count: Mapped[int]
    end_date: Mapped[datetime] = mapped_column(Date,
                                               nullable=True)


class Text(Base):
    __tablename__ = "texts"

    id: Mapped[intpk]
    text: Mapped[str] = mapped_column(String(1000))


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
