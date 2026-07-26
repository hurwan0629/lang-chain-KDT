from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_session
from models import Order, User
from schemas import ( OrderCreate, OrderResponse, UserCreate, UserResponse )

app = FastAPI()

# 연습용
# 실제 프로젝트에서는 Alembic 마이그레션을 사용하는 것이 일반적임
# Base에 등록되어있는 모든 스키마들에 대해서 생성을 요청하게 된다.
# Base.metadata.create_all(bind=engine)

@app.post("/users", response_model=UserResponse)
def create_user(
        body: UserCreate,
        session: Session = Depends(get_session),
):
    user = User(
        id=body.id,
        name=body.name
    )

    print("add 전:", user in session)

    session.add(user)

    print("new:", session.new)
    print("dirty:", session.dirty)
    print("deleted:", session.deleted)

    print("add 후:", user in session)

    # 세션에 쌓인 변경 내용을 DB에 전송하기
    # commit이 아님
    session.flush()

    # SERIAL / IDENTITY로 생성된 PK를
    # flush 후에는 확인할 수 있다.
    print("flush 후 PK:", user.pk)

    print("new:", session.new)
    print("dirty:", session.dirty)
    print("deleted:", session.deleted)

    session.commit()

    print("commit 후 user:", bool(user))

    print("new:", session.new)
    print("dirty:", session.dirty)
    print("deleted:", session.deleted)

    return user

@app.get("/users/{user_pk}", response_model=UserResponse)
def get_user(
    user_pk: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_pk)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@app.get("/users", response_model=list[UserResponse])
def get_users(
        session: Session = Depends(get_session)
):
    # 쿼리 작성할 재료 메서드 준비
    stmt = select(User)

    # 해당 쿼리 실행하기
    result = session.execute(stmt)

    # 실행하여 돌아온 결과에 대해서 전부 뽑아보기
    users = result.scalars().all()

    return users

@app.patch("/users/{user_pk}", response_model=UserResponse)
def update_user(
        user_pk: int,
        name: str,
        session: Session = Depends(get_session)
):
    user = session.get(User, user_pk)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    print("변경 전 dirty:", session.dirty)

    # ORM 객체 속성만 변경
    user.name = name

    # 별도로 session.add(user) 을 하지 않아도 된다.

    # user은 이미 persistent 상태이고
    # Session이 관리하고 있기 때문이다.
    print("변경 후 dirty:", session.dirty)

    session.commit()

    return user

@app.post("/orders", response_model=OrderResponse)
def create_order(
        body: OrderCreate,
        session: Session = Depends(get_session)
):
    # 주문을 만들기 전에 실제 사용자가 있는지 확인
    user = session.get(User, body.user_pk)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    order = Order(
        # user_pk=user.pk,
        user=user,
        total_price=body.total_price
    )

    session.add(order)

    session.commit()

    return order

@app.get("/users/{user_pk}/orders", status_code=200)
def get_user_orders(
        user_pk: int,
        session: Session = Depends(get_session)
):
    user = session.get(User, user_pk)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    print("user 조회 완료")

    # orders에 접근하는 순간 추가 SELECT가 발생할 수 있음
    orders = user.orders

    print("orders 접근 완료")

    return [
        {
            "pk": order.pk,
            "tootal_price": order.total_price
        }
        for order in orders
    ]
