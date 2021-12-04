import os
from dotenv import load_dotenv
from fastapi import FastAPI
import motor.motor_asyncio
from pydantic import BaseModel
from typing import Optional, List

load_dotenv()
app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://admin:{os.environ['MONGOPASSWORD']}@cluster0.kbeng.mongodb.net/PostcardsDB?retryWrites=true&w=majority")
db = client.PostcardsDB
collection = db.PostcardsCollection


# class Postcard(BaseModel):
#     id: int
#     url_front: Optional[str]
#     url_back: Optional[str]
#     text: Optional[str]
#     sent_date: Optional[str]
#     received_date: Optional[str]
#     from_address: Optional[str]
#     to_address: Optional[str]
#     lat_from: Optional[str]
#     lon_from: Optional[str]
#     lat_to: Optional[str]
#     lon_to: Optional[str]
#     sender_name: Optional[str]
#     receiver_name: Optional[str]
#     period: Optional[str]
#     tags: Optional[List[str]]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/postcards/")
async def get_all_postcards():
    postcards = await collection.find().to_list(100)
    return {"postcard": f"{postcards[1]}"}


@app.get("/postcards/{id}")
async def get_postcard_by_id(id: int):
    return {"postcard": f"Postcard {id}"}
