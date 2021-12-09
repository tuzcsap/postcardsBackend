import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://admin:{os.environ['MONGOPASSWORD']}@cluster0.kbeng.mongodb.net/PostcardsDB?retryWrites=true&w=majority")
db = client.PostcardsDB
collection = db.PostcardsCollection


# TODO define response model
class Postcard(BaseModel):
    _id: ObjectId
    id: int
    url_front: Optional[str]
    url_back: Optional[str]
    text_language: Optional[str]
    date_written: Optional[str]
    date_sent: Optional[str]
    date_received: Optional[str]
    address_from: Optional[str]
    address_to: Optional[str]
    country_from: Optional[str]
    country_to: Optional[str]
    settlement_from: Optional[str]
    settlement_to: Optional[str]
    name_from: Optional[str]
    name_to: Optional[str]
    lat_from: Optional[str]
    lng_from: Optional[str]
    lat_to: Optional[str]
    lng_to: Optional[str]
    time_period: Optional[str]
    tags: Optional[List[str]]


@app.get("/")
async def root():
    return {"message": "Hello World"}


# TODO filter postcards with null coords
# TODO error if no postcards were found
@app.get("/postcards", response_model=List[Postcard])
async def get_all_postcards():
    postcards = await collection.find().to_list(100)
    return {"postcard": f"{postcards[1]}"}


@app.get("/postcards/{id}", response_model=Postcard)
async def get_postcard_by_id(id: int):
    postcard = await collection.find_one({"id": id})
    return postcard
