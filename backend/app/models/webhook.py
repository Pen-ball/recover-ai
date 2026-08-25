from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from backend.app.db.database import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)
    razorpay_event_id = Column(String, unique=True, nullable=False, index=True)
    event_type = Column(String, nullable=False)
    payload_json = Column(JSON, nullable=True)

    processed_at = Column(DateTime(timezone=True), server_default=func.now())
