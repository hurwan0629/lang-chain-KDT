from app.database import Base, engine
from app.models import User, Order

# engine를 이용해서 Base의 메타데이터에 있는 ORM 객체들을 생성하기
Base.metadata.create_all(engine)


