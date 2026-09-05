from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session

from app.database import engine
from app.models import User

with Session(engine) as session:
    # stmt = select(User)

    # stmt = select(User).where(
    #     User.name == "lee"
    # )

    # stmt = (
    #     select(User)
    #     .where(User.id >= 5)
    #     .where(User.name == "lee")
    # )

    # stmt = select(User).where(
    #     User.name.in_(["customer1", "lee"])
    # )

    # stmt = select(User).where(
    #     or_(
    #         User.name == "customer1",
    #         User.id == 5
    #     )
    # )

    # stmt = select(User).where(
    #     and_(
    #         User.id >= 5,
    #         User.name == "lee"
    #     )
    # )

    # stmt = select(User).where(
    #     and_(
    #         User.id >= 3,
    #         User.id <= 5,
    #         or_(
    #             User.name == "customer1",
    #             User.name == "lee"
    #         )
    #     )
    # )

    # stmt = (
    #     select(User)
    #     .order_by(User.name.desc())
    #     .limit(2)
    # )

    # stmt = (
    #     select(User)
    #     .offset(1)
    #     .limit(2)
    # )

    stmt = select(User).order_by(User.id)

    print("type of stmt:", type(stmt))

    result = session.scalars(stmt)

    print("session identity_map before use:", session.identity_map.values())

    print("type of result:", type(result))
    # print("len of result:", len(result))

    users = result.all()
    # user = result.first()
    # user = result.one() # 하나가 아니면 예외
    # user = result.one_or_none() # 2개 이상이면 예외

    print("session identity_map after use:", session.identity_map.values())

    for user in users:
        print(user.id, user.name)

    # print(user.id, user.name)

    print(" --- session에서 get --- ")
    user2 = session.get(User, 5)
    print(user2.id, user2.name)

