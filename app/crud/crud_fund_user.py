from typing import Any, Dict, List, Optional, Union

from dateutil.parser import parse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.fund_user import FundUser
from app.schemas.fund_user import FundUserCreate, FundUserUpdate


class CRUDFundUser(CRUDBase[FundUser, FundUserCreate, FundUserUpdate]):
    def get_multi_by_fund(
        self,
        db: Session,
        *,
        fund_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundUser]:
        return (
            db.query(self.model)
            .filter(self.model.fund_id == fund_id)
            .all()
        )

fund_user = CRUDFundUser(FundUser)