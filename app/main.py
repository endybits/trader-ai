
import uvicorn
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi import FastAPI

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
    return HTMLResponse('<h1>FastAPI</h1>')



if __name__ == "__main__":

    uvicorn.run(app, host="localhost", port=8000)