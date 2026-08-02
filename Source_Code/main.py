from fastapi import FastAPI
from pydantic import BaseModel
from query import get_answer
from fastapi.middleware.cors import CORSMiddleware


class RequestBody(BaseModel):
    question: str

class ResponseBody(BaseModel):
    answer: str
    sources: list[str]
    file_headings: list[str]    
    
class HealthResponse(BaseModel):
    status: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_headers = ["*"],
    allow_methods = ["*"]
    )


@app.post("/ask", response_model=ResponseBody)
async def answer(request: RequestBody):
    
    response= get_answer(request.question)
    
    return {"answer": response['answer'], "sources": response['sources'], "file_headings": response['file_headings']}

@app.get("/health", response_model=HealthResponse)
async def get_health():
    return {"status": "ok"}

