from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class FundUserBase(BaseModel):
    timestamp: Optional[datetime] = None
    fund_id: Optional[int] = None
    user_id: Optional[int] = None


# Properties to receive on item creation
class FundUserCreate(FundUserBase):
    timestamp: datetime
    fund_id: int
    user_id: int


# Properties to receive on item update
class FundUserUpdate(FundUserBase):
    pass


# Properties shared by models stored in DB
class FundUserInDBBase(FundUserBase):
    timestamp: datetime
    fund_id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class FundUser(FundUserInDBBase):
    pass


# Properties properties stored in DB
class FundUserInDB(FundUserInDBBase):
    pass