from sqlalchemy import Column, DateTime, Integer, Float, JSON, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Fund(Base):
    """
    SQLAlchemy object :: `funds` table.

    Fields
    ------
    id : int
        The primary key and fund identifier.
    name : str
        The given name of fund.
    ...
    """

    __tablename__ = "funds"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    description = Column(String(516), nullable=False)
    max_collective_wagers = Column(Integer, nullable=False, default=3)
    max_capital_allocation = Column(Float, nullable=False, default=0.3)
    fund_quorum_threshold = Column(Float, nullable=False, default=0.2)
    details = Column(JSON, nullable=False)

    # relationships
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Fund `{self.id}`>"
