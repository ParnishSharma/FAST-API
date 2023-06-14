from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from models.todo import ToDo
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder



router = APIRouter()

# Configure MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["todo_app"]
collection = db["todos"]


@router.get("/")
def get_todos():
    todos = collection.find({}, {"_id": {"$toString": "$_id"},"name": 1, "description": 1})
    todo_list = [todo for todo in todos]
    return JSONResponse(content=todo_list)

@router.get("/{todo_name}")
def get_todo_by_name(todo_name: str):
    try:
        todo = collection.find_one({"name": todo_name})
        if todo:
            # Convert ObjectId to string representation
            todo["_id"] = str(todo["_id"])
            return todo
        else:
            raise HTTPException(status_code=404, detail="Todo not found", headers={"Error-Location": "todos"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.post("/")
def create_todo(todo: ToDo):
    todo_dict = todo.dict()
    result = collection.insert_one(todo_dict)
    todo_dict["_id"] = str(result.inserted_id)
    return todo_dict


@router.put("/")
def update_todo(todo_name: str, updated_todo: ToDo):
    updated_todo_dict = jsonable_encoder(updated_todo)
    result = collection.update_one({"name": todo_name}, {"$set": updated_todo_dict})
    if result.modified_count == 1:
        return {"message": "Todo updated successfully"}
    return {"error": "Todo not found"}



@router.delete("/delete/{todo_name}")
def delete_todo_by_name(todo_name: str):
    result = collection.delete_one({"name": todo_name})
    if result.deleted_count == 1:
        return {"message": "Todo deleted successfully"}
    return {"error": "Todo not found"}