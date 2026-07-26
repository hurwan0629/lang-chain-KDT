from sqlalchemy.orm import Session

from app.database import engine
from app.models import Profile, User

with Session(engine) as session:
    user = User(
        name="kim",
        email="park@test.com"
    )

    profile = Profile(
        bio="first profile",
        user=user
    )

    profile_err = Profile(
        bio="second profile",
        user=user
    )

    session.add(user)
    session.commit()

    print("user id:", user.id)
    print("profile id:", profile.id)
    print("profile user_id:", profile.user_id)