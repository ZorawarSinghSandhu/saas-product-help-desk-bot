from fastapi import FastAPI
from pydantic import BaseModel
from query import get_answer
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse




class RequestBody(BaseModel):
    question: str

class ResponseBody(BaseModel):
    answer: str
    sources: list[str]
    file_headings: list[str]    
    
class HealthResponse(BaseModel):
    status: str

app = FastAPI()

load_dotenv(override=True)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins = [ALLOWED_ORIGINS],
    allow_headers = ["*"],
    allow_methods = ["*"]
    )

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please wait a moment and try again."}
    )


@app.post("/ask", response_model=ResponseBody)
@limiter.limit("10/minute")
async def answer(request: Request, body: RequestBody):
    
    response= get_answer(body.question)
    
    return {"answer": response['answer'], "sources": response['sources'], "file_headings": response['file_headings']}

@app.get("/health", response_model=HealthResponse)
async def get_health():
    return {"status": "ok"}

