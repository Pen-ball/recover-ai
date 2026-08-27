# RecoverAI Deployment Guide

This guide details running RecoverAI both locally for development and containerized via Docker Compose.

## Environment Variables (.env)

Ensure a .env file exists in the root directory with the following variables:

DATABASE_URL=postgresql://postgres:postgrespassword@localhost:5432/recoverai
GEMINI_API_KEY=your_gemini_api_key_here
RAZORPAY_KEY_ID=your_razorpay_key_id_here
RAZORPAY_KEY_SECRET=your_razorpay_key_secret_here
RAZORPAY_WEBHOOK_SECRET=your_razorpay_webhook_secret_here

## Option 1: Docker Compose (Recommended for Testing/Production)

1. Ensure Docker Desktop is installed and running.
2. Build and start all services:
   docker-compose up --build -d
3. Access services:
   - Frontend Dashboard: http://localhost
   - Backend OpenAPI Docs: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
4. Stop all services:
   docker-compose down

## Option 2: Local Development Setup (Manual)

1. PostgreSQL Setup:
   - Ensure local PostgreSQL server is running.
   - Database name: recoverai

2. Backend Setup:
   - Activate venv: .\venv\Scripts\Activate.ps1
   - Install dependencies: pip install -r backend/requirements.txt
   - Run database migrations/tables: python backend/app/db/create_tables.py
   - Start backend server: uvicorn backend.app.main:app --reload --port 8000

3. Frontend Setup:
   - Navigate to frontend folder: cd frontend
   - Install dependencies: npm install
   - Start Vite dev server: npm run dev (http://localhost:5173)

4. Webhook Tunneling (for Razorpay Test Mode):
   - Start ngrok: ngrok http 8000
   - Update Razorpay Webhook URL with your ngrok HTTPS endpoint.
