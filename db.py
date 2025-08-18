from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]

def create_deal(deal):
    db.deals.insert_one(deal)

def get_deal(deal_id):
    return db.deals.find_one({"deal_id": deal_id})

def update_deal(deal_id, update):
    db.deals.update_one({"deal_id": deal_id}, {"$set": update})
