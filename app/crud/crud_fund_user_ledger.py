from typing import Any, Dict, List, Optional, Union

from dateutil.parser import parse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.fund import Fund
from app.models.fund_user import FundUser
from app.models.user import User
from app.models.fund_user_ledger import FundUserLedger
from app.schemas.fund_user_ledger import FundUserLedgerCreate, FundUserLedgerUpdate


class CRUDFundUserLedger(
    CRUDBase[FundUserLedger, FundUserLedgerCreate, FundUserLedgerUpdate]
):
    def create_with_owner(
        self,
        db: Session,
        *,
        obj_in: FundUserLedgerCreate,
        owner_id: int,
        fund_id: int
    ) -> FundUserLedger:

        # Get the request data
        obj_in_data = jsonable_encoder(obj_in)

        # Convert timestamp to a datetime object
        obj_in_data['timestamp'] = parse(obj_in_data['timestamp'])

        # Query user already belongs to the fund
        fund_user_query = (
            db.query(FundUser)
            .filter(
                FundUser.user_id == owner_id,
                FundUser.fund_id == fund_id
            )
        )

        # Create a FundUser if does not exist
        if not fund_user_query.scalar() is not None:
            new_fund_member = FundUser(
                fund_id=fund_id,
                user_id=owner_id
            )
            db.add(new_fund_member)
            db.commit()

        # Get the ID of FundUser
        fund_user = fund_user_query.first()

        # Push to database
        db_obj = self.model(**obj_in_data, fund_user_id=fund_user.id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_multi_by_owner(
        self,
        db: Session,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundUserLedger]:
        return (
            db.query(self.model)
            .join(FundUser, FundUserLedger.fund_user_id == FundUser.id)
            .filter(FundUser.user_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_fund_owner(
        self,
        db: Session,
        *,
        owner_id: int,
        fund_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundUserLedger]:
        return (
            db.query(self.model)
            .join(FundUser, FundUser.user_id == owner_id)
            .filter([
                FundUser.user_id == owner_id,
                FundUser.fund_id == fund_id
            ])
            .offset(skip)
            .limit(limit)
            .all()
        )


fund_user_ledger = CRUDFundUserLedger(FundUserLedger)
