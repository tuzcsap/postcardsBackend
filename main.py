import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import motor.motor_asyncio
from pymongo import MongoClient
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

client = MongoClient(
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
    return {"message": "Postcards Database"}


@app.get("/postcards", response_model=List[Postcard])
def get_all_postcards():
    postcards = []
    for postcard in collection.find():
        postcards.append(postcard)
    return postcards


@app.get("/postcards/filter", response_model=List[Postcard])
def get_filtered_postcards(time_period: str, settlement_from: str = "", settlement_to: str = ""):
    postcards = []
    query_dict = {"time_period": time_period}

    if settlement_from:
        query_dict["settlement_from"] = settlement_from
    if settlement_to:
        query_dict["settlement_to"] = settlement_to

    for postcard in collection.find(query_dict):
        postcards.append(postcard)
    return postcards



@app.get("/postcards/{id}", response_model=Postcard)
def get_postcard_by_id(id: int):
    postcard = collection.find_one({"id": id})
    return postcard


@app.get("/randompostcards", response_model=List[Postcard])
def get_random_postcards():
    postcards = []
    pipeline = [{"$sample": {"size": 2}}]
    for postcard in collection.aggregate(pipeline):
        postcards.append(postcard)
    return postcards


@app.get("/timeperiod", response_model=List[Postcard])
def get_postcard_by_time_period(time_period: str):
    postcards = []
    for postcard in collection.find({"time_period": time_period}):
        postcards.append(postcard)
    return postcards


@app.get("/cities/to")
def get_all_cities_to():
    cities = []
    for city in collection.distinct('settlement_to'):
        cities.append(city)
    return cities


@app.get("/cities/from")
def get_all_cities_from():
    cities = []
    for city in collection.distinct('settlement_from'):
        cities.append(city)
    return cities
