from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import customers, transactions, webhooks, dashboard

app = FastAPI(title="RecoverAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://YOUR-VERCEL-URL-WILL-GO-HERE.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(webhooks.router)
app.include_router(dashboard.router)


@app.get("/")
def read_root():
    return {"message": "RecoverAI backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
