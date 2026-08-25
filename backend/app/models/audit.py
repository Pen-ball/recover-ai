from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.app.db.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)

    event = Column(String, nullable=False)
    decision = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    policy_decision = Column(String, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
