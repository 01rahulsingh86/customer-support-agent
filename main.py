from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent import ask_agent


app = FastAPI(
    title="CloudCart Customer Support API",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = ask_agent(request.message)
    return ChatResponse(answer=answer)
