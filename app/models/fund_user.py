from sqlalchemy import Column, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from app.db.base_class import Base


class FundUser(Base):
    """
    SQLAlchemy object :: `fund_users` table.

    Represents a lookup table for which users belong to what funds. A user
    can be a member of multiple funds. There exists a unique index on the
    combination of a user and a fund.

    Fields
    ------
    id : int
        The primary key and fund user identifier.
    fund_id : int
        The fund identifier.
    user_id : int
        The user identifier.
    """

    __tablename__ = "fund_users"
    __table_args__ = (
        UniqueConstraint(
            'fund_id',
            'user_id',
            name='unique_idx_fund_id_user_id'
        ),
    )

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    fund_id = Column(Integer, ForeignKey("funds.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<FundUser `{self.id}`>"