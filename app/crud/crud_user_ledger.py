from typing import Any, Dict, List, Optional, Union

from dateutil.parser import parse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user_ledger import UserLedger
from app.schemas.user_ledger import UserLedgerCreate, UserLedgerUpdate


class CRUDUserLedger(CRUDBase[UserLedger, UserLedgerCreate, UserLedgerUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: UserLedgerCreate, owner_id: int
    ) -> UserLedger:
        obj_in_data = jsonable_encoder(obj_in)
        # Convert timestamp to a datetime object
        obj_in_data['timestamp'] = parse(obj_in_data['timestamp'])
        db_obj = self.model(**obj_in_data, user_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserLedger]:
        return (
            db.query(self.model)
            .filter(UserLedger.user_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


user_ledger = CRUDUserLedger(UserLedger)