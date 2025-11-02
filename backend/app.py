from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_model import AIModel
from database import init_sample_data
from csv_processor import csv_processor
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Stock Support Chatbot", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI model
ai_model = AIModel()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    success: bool
    stock_code: str = None
    notional_amount: float = None
    query_date: str = None

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    init_sample_data()
    # Check if data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Created data directory. Please add your CSV log files.")
    print("Backend server started with CSV processing capability!")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = ai_model.process_query(request.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "huggingface"}

@app.get("/models/status")
async def model_status():
    """Check if models are loaded properly"""
    status = {
        "sentence_model_loaded": ai_model.sentence_model is not None,
        "chat_model_loaded": ai_model.chat_model is not None,
        "chat_pipeline_loaded": ai_model.chat_pipeline is not None
    }
    return status

@app.get("/data/available-dates")
async def get_available_dates():
    """Get available dates from CSV files"""
    dates = csv_processor.get_available_dates()
    return {"available_dates": [d.isoformat() for d in dates]}

@app.get("/data/available-stocks")
async def get_available_stocks(date: str = None):
    """Get available stocks for a specific date"""
    from datetime import datetime
    query_date = datetime.strptime(date, "%Y-%m-%d").date() if date else None
    stocks = csv_processor.get_available_stocks(query_date)
    return {"stocks": stocks, "date": date}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=debug)