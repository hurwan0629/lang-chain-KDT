from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_CLIENT_ID = None
try:
    OPENAI_CLIENT_ID = os.environ["OPENAI_CLIENT_ID"]
except Exception as e:
    print(e)
    print("OPENAI_CLIENT_ID does not exists")


MONGO_URL = None
try:
    MONGO_URL = os.environ["MONGO_URL"]
except Exception as e:
    print(e)
    print("MONGO_URL does not exists")


MONGO_DATABASE = None
try:
    MONGO_DATABASE = os.environ["MONGO_DATABASE"]
except Exception as e:
    print(e)
    print("MONGO_DATABASE does not exists")


MONGO_TABLE = None
try:
    MONGO_TABLE = os.environ["MONGO_TABLE"]
except Exception as e:
    print(e)
    print("MONGO_TABLE does not exists")