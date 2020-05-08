from typing import Any, Dict, List, Optional, Union

from dateutil.parser import parse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.fund import Fund
from app.schemas.fund import FundCreate, FundUpdate


class CRUDFund(CRUDBase[Fund, FundCreate, FundUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: FundCreate, owner_id: int
    ) -> Fund:
        obj_in_data = jsonable_encoder(obj_in)
        # Convert timestamp to a datetime object
        obj_in_data['timestamp'] = parse(obj_in_data['timestamp'])

        # TODO: Add JSONSchema to validate `details` key.
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Fund]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

fund = CRUDFund(Fund)
