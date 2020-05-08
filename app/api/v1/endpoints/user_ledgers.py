from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.UserLedger])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user ledger transactions.
    """
    if crud.user.is_superuser(current_user):
        transactions = crud.user_ledger.get_multi(db, skip=skip, limit=limit)
    else:
        transactions = crud.user_ledger.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return transactions


@router.post("/", response_model=schemas.UserLedger)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: schemas.UserLedgerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    transaction = crud.user_ledger.create_with_owner(
        db=db,
        obj_in=transaction_in,
        owner_id=current_user.id
    )
    return transaction


@router.get("/{id}", response_model=schemas.UserLedger)
def read_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    transaction = crud.user_ledger.get(db=db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if not crud.user.is_superuser(current_user) and (transaction.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return transaction