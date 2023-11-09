
import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from fastapi.responses import HTMLResponse
from fastapi import WebSocket

from utils.html_response import html
from utils.langchain_labs import text2sql
from app.utils.db_querier import exec_query

class UserQuery(BaseModel):
    user_id: str = Field(..., example="123")
    question: str = Field(
        ...,
        min_length=8,
        example="which hour of the day is best to trade on tuesday in 2023? also show pnl grouped by other hours of the day",
    )


app = FastAPI()

@app.get("/")
async def root():
    '''This function returns the HTML response for the main page'''
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    '''This function handles the websocket connection and the communication between the client and the server'''
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        data = await websocket.receive_json()
        user_query = json.loads(data)
        question: str = user_query.get("question")
        user_id = user_query.get("user_id")
        await websocket.send_text(f"{question.capitalize()}")
        await websocket.send_text(f"loading")
        sql_command = await text2sql(user_id, question)
        await websocket.send_text(f"{sql_command}")
        data_res = exec_query(sql_command)
        await websocket.send_text(f"{data_res}")


if __name__ == "__main__":

    uvicorn.run(app, host="localhost", port=8000)