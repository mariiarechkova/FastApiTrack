from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    users = relationship(
        "User",
        back_populates="organisation",
        passive_deletes=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Organisation name={self.name}>"
