from sqlalchemy import Column, DateTime, Float, Integer, ForeignKey
from sqlalchemy.sql import func

from app.db.base_class import Base


class FundUserLedger(Base):
    """
    SQLAlchemy object :: `fund_user_ledgers` table.

    Fields
    ------
    id : int
        The primary key and fund user ledger identifier.
    fund_user_id : int
        The fund user identifier.
    amount : float
        Transaction value.
    timestamp : datetime
        Timestamp of transaction.
    """

    __tablename__ = "fund_user_ledgers"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())

    # relationships
    fund_user_id = Column(Integer, ForeignKey("fund_users.id"), nullable=False)

    def __repr__(self):
        return f"<FundUserLedger `{self.id}`>"
