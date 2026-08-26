from fastapi import FastAPI
from backend.app.api import customers, transactions, webhooks

# Create the FastAPI application instance.
# This "app" object is what Uvicorn will run.
app = FastAPI(title="RecoverAI Backend")

# Register routers so their endpoints become part of this app.
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(webhooks.router)


# A basic root endpoint - just to confirm the server is alive.
@app.get("/")
def read_root():
    return {"message": "RecoverAI backend is running"}


# A health check endpoint.
# In real systems, monitoring tools ping this to check if the service is up.
@app.get("/health")
def health_check():
    return {"status": "ok"}
