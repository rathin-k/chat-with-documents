from app.database.mongodb import db
from app.utils.security import hash_password
from app.utils.security import verify_password, create_access_token

users_collection = db["users"]

def create_user(user):
    existing_user = users_collection.find_one(
      {
        "email": user.email
      }
    )

    if existing_user:
     return None

    hashed_password = hash_password(user.password)

    user_document = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
    }

    result = users_collection.insert_one(user_document)

    return str(result.inserted_id)

def login_user(user):
    existing_user = users_collection.find_one(
        {
            "email": user.email
        }
    )

    if not existing_user:
        return None

    if not verify_password(
        user.password,
        existing_user["password"]
    ):
        return None

    access_token = create_access_token(
        {
            "sub": str(existing_user["_id"]),
            "email": existing_user["email"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }