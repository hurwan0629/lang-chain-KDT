from fastapi import APIRouter
from sqlalchemy import select

from .dto import users

from database.database import SessionFactory
from database.models import Users

router = APIRouter(
    prefix="/router",
    tags=["router"]
)

@router.get("/health")
def healthCheck():
    print("router/test_router.py healthCheck")
    return {
        "message": "healthy"
    }

@router.post("/user")
def createUser(request: users.CreateUserRequest):
    print("create user:", request)

    with SessionFactory() as session:
        print("session start")

        user = Users(name = request.name, id = request.id)

        stmt = select(Users)

        results = session.scalars(stmt).all()


        print("1. result[first]:")
        print("result length:", len(results))

        for r in results:
            print(r)


        session.add(user)

        results = session.scalars(stmt).all()

        print("2. result[added]:")
        print("result length:", len(results))
        for r in results:
            print(r)

        session.refresh(user)

        results = session.scalars(stmt).all()

        print("3. result:")
        print("result length:", len(results))
        for r in results:
            print(r)

        session.commit()
        session.refresh(user)

        response = {
            "message": "created",
            "pk": user.pk,
            "id": user.id,
            "name": user.name,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    return response