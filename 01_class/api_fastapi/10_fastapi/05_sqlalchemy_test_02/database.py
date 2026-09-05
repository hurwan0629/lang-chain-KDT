from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "postgresql+psycopg2://hurwan:1234@localhost:5432/testdb"

# 모든 ORM의 부모 클래스
class Base(DeclarativeBase):
    pass

# Engine
# SQLAlchemy와 실제 DB 사이의 연결 관리자
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Session을 찍어내는 factory
SessionLocal = sessionmaker(
    bind=engine,

    # commit 이후 ORM 객체를 자동 expire 시키지 않는 것
    expire_on_commit=False
    # 아까 ORM객체가 자동으로 expire 되어서 잠깐 헤매었었음
)

def get_session() -> Generator[Session, None, None]:
    """
    요청 하나당 Session 하나를 만들어주는 dependency

    1. 요청 시작
    2. Session 생성
    3. API 작업
    4. API 종료
    5. finally에서 Session.close()
    """

    session = SessionLocal()

    try:
        yield session
    finally:
        # Session이 잡고있던 자원을 정리/반한
        session.close()
