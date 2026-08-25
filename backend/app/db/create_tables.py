from backend.app.db.database import engine, Base

# Import all models so SQLAlchemy knows about them before creating tables
from backend.app.models.customer import Customer
from backend.app.models.transaction import Transaction
from backend.app.models.recovery import RecoveryCase
from backend.app.models.action import RecoveryAction
from backend.app.models.audit import AuditLog
from backend.app.models.webhook import WebhookEvent

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Done! Tables created successfully.")
