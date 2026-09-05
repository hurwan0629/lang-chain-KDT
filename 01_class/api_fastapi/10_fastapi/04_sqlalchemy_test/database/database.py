from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL="postgresql+psycopg2://hurwan:1234@localhost:5432/testdb"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=True
)

class Base(DeclarativeBase):
    pass
