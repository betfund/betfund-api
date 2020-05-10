from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class FundUserLedgerBase(BaseModel):
    amount: Optional[float] = None
    timestamp: Optional[datetime] = None


# Properties to receive on item creation
class FundUserLedgerCreate(FundUserLedgerBase):
    amount: float
    timestamp: datetime


# Properties to receive on item update
class FundUserLedgerUpdate(FundUserLedgerBase):
    pass


# Properties shared by models stored in DB
class FundUserLedgerInDBBase(FundUserLedgerBase):
    id: int
    amount: float
    timestamp: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class FundUserLedger(FundUserLedgerInDBBase):
    pass


# Properties properties stored in DB
class FundUserLedgerInDB(FundUserLedgerInDBBase):
    pass