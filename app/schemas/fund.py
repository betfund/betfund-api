from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class FundBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    timestamp: Optional[datetime] = None
    details: Optional[dict] = None
    owner_id: Optional[int] = None


# Properties to receive on item creation
class FundCreate(FundBase):
    name: str
    description: str
    timestamp: datetime
    details: dict


# Properties to receive on item update
class FundUpdate(FundBase):
    pass


# Properties shared by models stored in DB
class FundInDBBase(FundBase):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    timestamp: Optional[datetime] = None
    details: Optional[dict] = None
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Fund(FundInDBBase):
    pass


# Properties properties stored in DB
class FundInDB(FundInDBBase):
    pass