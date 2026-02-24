from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

class CommentRequest(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    sentiment: str
    rating: int

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "rating": {"type": "integer", "minimum": 1, "maximum": 5}
    },
    "required": ["sentiment", "rating"],
    "additionalProperties": False
}

@app.post("/comment", response_model=SentimentResponse)
async def analyze_comment(request: CommentRequest):
    # Mock sentiment analysis (works without OpenAI!)
    comment_lower = request.comment.lower()
    
    if any(word in comment_lower for word in ['amazing', 'love', 'great', 'excellent', 'perfect']):
        return SentimentResponse(sentiment="positive", rating=5)
    elif any(word in comment_lower for word in ['sucks', 'hate', 'terrible', 'worst', 'awful']):
        return SentimentResponse(sentiment="negative", rating=1)
    elif any(word in comment_lower for word in ['ok', 'fine', 'average', 'meh']):
        return SentimentResponse(sentiment="neutral", rating=3)
    elif any(word in comment_lower for word in ['good', 'nice']):
        return SentimentResponse(sentiment="positive", rating=4)
    else:
        return SentimentResponse(sentiment="neutral", rating=3)


@app.get("/")
async def root():
    return {"message": "Sentiment API ready!"}
