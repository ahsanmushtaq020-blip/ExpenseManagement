from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://expense:expense@cluster0.xuf76pr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

db = client["expense_tracker"]

user_collection = db["users"]
expense_collection = db["expenses"]
income_collection = db["income"]