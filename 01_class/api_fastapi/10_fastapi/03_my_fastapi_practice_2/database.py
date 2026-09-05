from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE = "postgresql+psycopg://postgres:1234@localhost:5432/todo"

engine = create_engine(
    DATABASE,
    echo=True,
)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)