from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.app.db.database import Base


class RecoveryAction(Base):
    __tablename__ = "recovery_actions"

    id = Column(Integer, primary_key=True, index=True)
    recovery_case_id = Column(Integer, ForeignKey("recovery_cases.id"), nullable=False)

    action_type = Column(String, nullable=False)
    action_reason = Column(String, nullable=True)
    risk_score = Column(Float, nullable=True)
    expected_value = Column(Float, nullable=True)
    policy_status = Column(String, nullable=False)

    executed_at = Column(DateTime(timezone=True), server_default=func.now())
    result = Column(String, nullable=True)
