import uvicorn
from fastapi import FastAPI, Path, Body

from libs import database
from models.message import Message


app = FastAPI()
Path()

@app.on_event("startup")
def on_startup():
    database.init_tables()

@app.post("/chat/{chat_id}")
async def new_message(chat_id, body: Bod)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5500)