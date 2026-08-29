from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime




class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None




class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    lifetime_value: float
    total_transactions: int
    successful_transactions: int
    failed_transactions: int
    average_transaction_value: float
    last_payment_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
