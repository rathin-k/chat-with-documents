from pymongo import MongoClient

uri = "mongodb+srv://csvc9b12rathin_db_user:Collab123@cluster0.8emirpq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(uri)
    client.admin.command("ping")
    print("✅ Connected Successfully!")
except Exception as e:
    print("❌ Connection Failed")
    print(e)