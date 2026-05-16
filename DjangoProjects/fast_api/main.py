from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': "Hello World"}


#routingh endpoints
@app.get("/users")
def get_users():
    return ['Ali', 'Vali']

@app.get("/products")
def get_products():
    return ['Phone', 'Laptop']


# Path Parameter  (http://127.0.0.1:8000/users/5) <- shu bilan ishlaydi
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# Query Parameter (http://127.0.0.1:8000/items/?skip=5&limit=6) <- urlda
@app.get('/items/')
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

class User(BaseModel):
    id: Optional[int] = None
    name: str
    age: int

db: List[User] = []


# CREATE (POST)
@app.post('/users')
def create_users(user: User):
    user.id = len(db) + 1
    db.append(user)
    return {"message": "User create", "data": user}

# READ (GET)
@app.get("/users")
def get_users():
    return db

# UPDATE (PUT)
@app.put('/users/{user_id}')
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate:
        if user.id == user_id:
            updated_user.id = user_id
            db[index] = updated_user
            return {"message": "Update", "data": updated_user}
    raise HTTPException(status_code=404, detail="User not found")

# DELETE
@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    for index, user in enumerate(db):
        if user.id == user_id:
            db.pop(index)
            return {"mesage": "Deleted"}
    raise HTTPException(status_code=404, detail="User not found")