from datetime import datetime

from pymongo import MongoClient

from app import config


__client=None
__db=None
__datas=None

try:
    __client = MongoClient(config.MONGO_URL)
    print("db connected:", __db)
    __db = __client[config.MONGO_DATABASE]
    print("db created:", __db)
    __datas=__db[config.MONGO_TABLE]

except Exception as e:
    print("database error:", e)



def insert_data(
    product_name: str,
    details: str,
    tone_and_manner: str,
    ad: str,
    created_at: datetime,
):
    data = {
      "user_req": {
        "product_name": product_name,
        "details": details,
        "tone_and_manner": tone_and_manner,
      },
      "server_res": {
        "ad": ad,
        "created_at": created_at,
      }
    }

    print("database insert_data():", data)

    created_data = None

    if __datas is not None:
        result = __datas.insert_one(data)
        print("database insert_data() inserted:", result.inserted_id)

        created_data = __datas.find_one(
            {"_id": result.inserted_id},
            {"_id": 0}
        )

        print("database insert_data() created_data:", created_data)

    return created_data

def get_all_data():
    print("database get_all_data() start")
    datas = list(
        __datas
        .find({}, {"_id": 0})
        .sort("server_res.created_at", -1))



    print("database get_all_data() selected")
    print("  datas:", datas)

    return datas
