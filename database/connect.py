from pymongo import MongoClient
from data.config import mongodb_url


client = MongoClient(mongodb_url)
db = client["support"]

db_supporters = db.supporters


async def db_close():
    client.close()
