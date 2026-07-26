from sqlalchemy import inspect

from app.models import User, Order

user_mapper = inspect(User)
order_mapper = inspect(Order)

print(" --- User relationships --- ")
for rel in user_mapper.relationships:
    print("name:", rel.key)
    print("target:", rel.mapper.class_)
    print("direction:", rel.direction)
    print("join:", rel.primaryjoin)

print()

print(" --- Order foreign keys --- ")
for fk in Order.__table__.foreign_keys:
    print("FK:", fk)
    print("target:", fk.target_fullname)
