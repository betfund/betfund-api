from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{fund_id}", response_model=schemas.Fund)
def read_fund_users(
    *,
    db: Session = Depends(deps.get_db),
    fund_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get fund by ID.
    """
    fund_users = crud.fund_user.get_multi_by_fund(db=db, fund_id=fund_id)
    if not fund_users:
        raise HTTPException(status_code=404, detail="Fund users not found")
    return fund_users
