from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = (
    "postgresql+psycopg2://hurwan:1234@127.0.0.1:5432/test"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)

class Base(DeclarativeBase):
    pass

