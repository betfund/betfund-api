from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserLedgerBase(BaseModel):
    amount: Optional[float] = None
    timestamp: Optional[datetime] = None


# Properties to receive on item creation
class UserLedgerCreate(UserLedgerBase):
    amount: float
    timestamp: datetime


# Properties to receive on item update
class UserLedgerUpdate(UserLedgerBase):
    pass


# Properties shared by models stored in DB
class UserLedgerInDBBase(UserLedgerBase):
    id: int
    amount: float
    timestamp: datetime
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class UserLedger(UserLedgerInDBBase):
    pass


# Properties properties stored in DB
class UserLedgerInDB(UserLedgerInDBBase):
    pass