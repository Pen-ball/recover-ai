from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.app.db.database import Base


class RecoveryCase(Base):
    __tablename__ = "recovery_cases"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)

    revenue_at_risk = Column(Float, nullable=False)
    recovery_probability = Column(Float, nullable=True)
    recommended_action = Column(String, nullable=True)
    expected_recovery = Column(Float, nullable=True)
    actual_recovery = Column(Float, nullable=True)

    status = Column(String, default="open")
    retry_count = Column(Integer, default=0)
    escalation_level = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
