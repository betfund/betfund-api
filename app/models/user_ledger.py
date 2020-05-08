from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserLedger(Base):
    """SQLAlchemy object for `user_ledgers` table.

    Fields
    ------
    id : int
        The primary key and user identifier.
    user_id : int
        The user identifier.
    amount : float
        Transaction value.
    timestamp : datetime
        Timestamp of transaction.
    """

    __tablename__ = "user_ledgers"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())

    # relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<UserLedger `{self.id}`>"