# Stock Support Chatbot

AI-powered chatbot application for stock trading support that can analyze CSV log files and provide real-time trading information.

## Features

- AI-Powered Conversations: Uses Hugging Face models for natural language processing
- CSV Log Processing: Automatically reads and analyzes trading log files
- Date Intelligence: Understands natural language dates (today, yesterday, specific dates)
- Real-time Data: Calculates notional amounts, volumes, and prices from trade data
- Modern UI: Clean, responsive chat interface with dark theme
- Local Processing: No external API dependencies for AI models

## 📁 Project Structure

chatbot-app/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx          # Main chat component
│   │   ├── main.tsx         # React entry point
│   │   └── index.css        # Styling
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── backend/                  # FastAPI Python backend
│   ├── app.py               # FastAPI server
│   ├── ai_model.py          # AI model handling
│   ├── csv_processor.py     # CSV log processing
│   ├── database.py          # Database models
│   ├── data/                # CSV log files
│   │   ├── ClientExecution_20251025.csv
│   │   ├── ClientExecution_20251026.csv
│   │   └── ClientExecution_20251027.csv
│   ├── requirements.txt
│   └── .env
└── README.md

## 🛠️ Setup Instructions

### Prerequisites

- Node.js (v16 or higher) - Download from nodejs.org
- Python (v3.8 or higher) - Download from python.org

### Manual Setup

#### Backend Setup

1. Navigate to backend folder
   cd backend

2. Run backend setup
   setup-backend.bat

3. Create sample data (if needed)
   create_sample_data.bat

4. Start backend server
   start-backend.bat
   Backend will run on: http://localhost:8000

#### Frontend Setup

1. Navigate to frontend folder
   cd frontend

2. Run frontend setup
   setup-frontend.bat

3. Start frontend server
   start-frontend.bat
   Frontend will run on: http://localhost:3000

## 📊 CSV Log File Format

The application expects CSV files in the backend/data/ directory with the following format:

Timestamp;ClientName;AccountName;Instrument;Quantity;Price
09:30:15.048448;ABC;ABC_account;0148.HK;10000;27.44
10:15:22.123456;XYZ;XYZ_invest;0148.HK;5000;27.50

File Naming Convention:
- ClientExecution_YYYYMMDD.csv
- Example: ClientExecution_20251025.csv

Required Columns:
- Timestamp - Trade timestamp
- ClientName - Client identifier
- AccountName - Account identifier
- Instrument - Stock code (e.g., 0148.HK)
- Quantity - Number of shares traded
- Price - Trade price per share

## 💬 Example Queries

Stock Notional Queries:
- "What is the notional traded for 0148.HK?"
- "Show me today's trading for 0700.HK"
- "How much was traded for 0148.HK yesterday?"
- "What was the notional amount for 0148.HK on 2025-10-25?"

Date-Based Queries:
- "What data do you have for yesterday?"
- "Show me available trading dates"
- "What stocks were traded on 2025-10-26?"

General Queries:
- "Hello, what can you help me with?"
- "What trading information can you provide?"

## 🔧 API Endpoints

Chat Endpoints:
- POST /chat - Process user messages
- GET /health - Health check
- GET /models/status - AI model status

Data Endpoints:
- GET /data/available-dates - List available trading dates
- GET /data/available-stocks - List stocks for a specific date

## 💬 Key Components

Backend Services:

1. CSV Processor (csv_processor.py)
   - Reads and parses trading log files
   - Extracts dates from filenames
   - Calculates notional amounts (Quantity × Price)
   - Filters data by stock and date

2. AI Model (ai_model.py)
   - Uses Hugging Face models for NLP
   - Extracts stock codes and dates from queries
   - Classifies user intent
   - Generates natural responses

3. FastAPI Server (app.py)
   - REST API endpoints
   - CORS configuration
   - Error handling

Frontend Features:
- Modern Chat Interface - Message bubbles with user/bot differentiation
- Real-time Status - Backend connection and model status
- Quick Questions - Predefined common queries
- Responsive Design - Works on desktop and mobile
- Error Handling - Clear error messages and retry options

## 🔄 Adding New CSV Data

1. Place new CSV files in backend/data/ directory
2. Follow naming convention: ClientExecution_YYYYMMDD.csv
3. Ensure correct format (semicolon delimited)
4. Restart backend server to load new data

## 🚀 Deployment

Development:
- Use the provided batch scripts for local development
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
 
