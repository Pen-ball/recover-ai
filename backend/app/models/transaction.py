from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    razorpay_payment_id = Column(String, unique=True, nullable=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    payment_method = Column(String, nullable=True)
    status = Column(String, nullable=False)

    failure_reason = Column(String, nullable=True)
    failure_code = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
