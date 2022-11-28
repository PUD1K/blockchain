from typing import Union

from multiprocessing.dummy import Process
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from start import User
import json
from fastapi.middleware.cors import CORSMiddleware
import time


app = FastAPI()


class user_data:
    def __init__(self, username, password):
        self.user = User(username, password)
        self.my_hach = str(self.user.hach)
        self.my_coins = str(self.user.check_coins())

class messageBody(BaseModel):
    from_hach: str
    to_hach: str
    message: str

class coinsBody(BaseModel):
    from_hach: str
    to_hach: str
    count_coins: str
    

username = "tum"
password = "1"
user_data = user_data(username, password)

@app.post("/send_message")
async def send_message(body: messageBody):
    data = {
        "type_task": "custom",
        "from_hach": body.from_hach,
        "to_hach": body.to_hach,
        "message": body.message
    }
    result = user_data.user.send_task(data)
    return result


@app.post("/send_coins")
async def send_message(body: coinsBody):
    data = {
        "type_task": "send_coins",
        "from_hach": body.from_hach,
        "to_hach": body.to_hach,
        "count_coins": body.count_coins
    }
    result = user_data.user.send_task(data)
    return result


@app.get("/get_tasks")
async def get_tasks():
    return user_data.user.get_tasks()

@app.get("/do_tasks")
async def do_tasks():
    user_data.user.do_tasks_value = True
    # user_data.user.do_tasks()

    process = Process(target = user_data.user.do_tasks)
    process.start()
    print('popa')
    # time.sleep(300)
    # user_data.user.do_tasks_value = False

@app.get("/stop_tasks")
async def stop_tasks():
    user_data.user.do_tasks_value = False

@app.get("/get_chains")
async def get_chains():
    return user_data.user.get_chains()

@app.get("/update_coins")
async def update_coins():
    user_data.my_coins = user_data.user.check_coins()
    return {"coins" : user_data.my_coins}

@app.get("/my_data")
async def my_data():
    data = {
        "username": "tum",
        'hach': user_data.my_hach,
        'coins': user_data.my_coins
    }
    return data
    



origins = [
    "http://localhost:8080",
    "http://128.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

