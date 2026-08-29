from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class TransactionCreate(BaseModel):
    customer_id: int
    amount: float
    currency: str = "INR"
    payment_method: Optional[str] = None
    status: str
    failure_reason: Optional[str] = None
    failure_code: Optional[str] = None
    razorpay_payment_id: Optional[str] = None



class TransactionResponse(BaseModel):
    id: int
    razorpay_payment_id: Optional[str] = None
    customer_id: int
    amount: float
    currency: str
    payment_method: Optional[str] = None
    status: str
    failure_reason: Optional[str] = None
    failure_code: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
