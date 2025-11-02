Stock Support Chatbot
A modern, AI-powered chatbot application for stock trading support that can analyze CSV log files and provide real-time trading information.

🚀 Features
AI-Powered Conversations: Uses Hugging Face models for natural language processing

CSV Log Processing: Automatically reads and analyzes trading log files

Date Intelligence: Understands natural language dates (today, yesterday, specific dates)

Real-time Data: Calculates notional amounts, volumes, and prices from trade data

Modern UI: Clean, responsive chat interface with dark theme

Local Processing: No external API dependencies for AI models

📁 Project Structure
text
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
🛠️ Setup Instructions
Prerequisites
Node.js (v16 or higher) - Download here

Python (v3.8 or higher) - Download here

Git - Download here

Quick Start (Windows)
Clone or Download the Project

bash
# If using Git
git clone <repository-url>
cd chatbot-app
Run Master Setup

bash
# Double-click this file in Windows Explorer
setup-project.bat
This will automatically set up both backend and frontend.

Start the Application

bash
# Double-click this file
start-app.bat
Manual Setup
Backend Setup
Navigate to backend folder

bash
cd backend
Run backend setup

bash
setup-backend.bat
Create sample data (if needed)

bash
create_sample_data.bat
Start backend server

bash
start-backend.bat
Backend will run on: http://localhost:8000

Frontend Setup
Navigate to frontend folder

bash
cd frontend
Run frontend setup

bash
setup-frontend.bat
Start frontend server

bash
start-frontend.bat
Frontend will run on: http://localhost:3000

📊 CSV Log File Format
The application expects CSV files in the backend/data/ directory with the following format:

csv
Timestamp;ClientName;AccountName;Instrument;Quantity;Price
09:30:15.048448;ABC;ABC_account;0148.HK;10000;27.44
10:15:22.123456;XYZ;XYZ_invest;0148.HK;5000;27.50
File Naming Convention:

ClientExecution_YYYYMMDD.csv

Example: ClientExecution_20251025.csv

Required Columns:

Timestamp - Trade timestamp

ClientName - Client identifier

AccountName - Account identifier

Instrument - Stock code (e.g., 0148.HK)

Quantity - Number of shares traded

Price - Trade price per share

💬 Example Queries
Stock Notional Queries
"What is the notional traded for 0148.HK?"

"Show me today's trading for 0700.HK"

"How much was traded for 0148.HK yesterday?"

"What was the notional amount for 0148.HK on 2025-10-25?"

Date-Based Queries
"What data do you have for yesterday?"

"Show me available trading dates"

"What stocks were traded on 2025-10-26?"

General Queries
"Hello, what can you help me with?"

"What trading information can you provide?"

🔧 API Endpoints
Chat Endpoints
POST /chat - Process user messages

GET /health - Health check

GET /models/status - AI model status

Data Endpoints
GET /data/available-dates - List available trading dates

GET /data/available-stocks - List stocks for a specific date

🎯 Key Components
Backend Services
CSV Processor (csv_processor.py)

Reads and parses trading log files

Extracts dates from filenames

Calculates notional amounts (Quantity × Price)

Filters data by stock and date

AI Model (ai_model.py)

Uses Hugging Face models for NLP

Extracts stock codes and dates from queries

Classifies user intent

Generates natural responses

FastAPI Server (app.py)

REST API endpoints

CORS configuration

Error handling

Frontend Features
Modern Chat Interface - Message bubbles with user/bot differentiation

Real-time Status - Backend connection and model status

Quick Questions - Predefined common queries

Responsive Design - Works on desktop and mobile

Error Handling - Clear error messages and retry options

🐛 Troubleshooting
Common Issues
Backend Connection Failed

Ensure backend is running on port 8000

Check if start-backend.bat completed successfully

Verify Python virtual environment is activated

AI Models Not Loading

First-time setup downloads models (may take 5-10 minutes)

Check internet connection for initial download

Models are cached locally after first download

CSV Files Not Found

Ensure CSV files are in backend/data/ directory

Verify file naming convention: ClientExecution_YYYYMMDD.csv

Check CSV format (semicolon delimited)

Port Already in Use

Backend: Change PORT in backend/.env

Frontend: Change port in frontend/vite.config.js

Logs and Debugging
Backend logs appear in the backend command window

Frontend errors appear in browser console (F12)

Model loading status shown in the UI status bar

🔄 Adding New CSV Data
Place new CSV files in backend/data/ directory

Follow naming convention: ClientExecution_YYYYMMDD.csv

Ensure correct format (semicolon delimited)

Restart backend server to load new data

📝 Environment Variables
Backend (.env)
env
DATABASE_URL=sqlite:///./stock_trades.db
DEBUG=True
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
Frontend (.env)
env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Stock Support Chatbot
🚀 Deployment
Development
Use the provided batch scripts for local development

Backend: http://localhost:8000

Frontend: http://localhost:3000

Production Considerations
Use production-grade WSGI server (e.g., Gunicorn)

Set DEBUG=False in production

Configure proper CORS origins

Use production database (PostgreSQL/MySQL)

Set up proper logging and monitoring