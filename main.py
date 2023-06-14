
from routers import todos
from pymongo import MongoClient
import subprocess
subprocess.run(["pip", "install", "--no-cache-dir", "-r", "requirements.txt"])
from fastapi import FastAPI
app = FastAPI()

# Configure MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["todo_app"]
collection = db["todos"]

# Include the todos router
app.include_router(todos.router)
