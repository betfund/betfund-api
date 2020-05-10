from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.FundUserLedger])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve fund user ledger transactions.
    """
    if crud.user.is_superuser(current_user):
        transactions = crud.fund_user_ledger.get_multi(
            db,
            skip=skip,
            limit=limit
        )
    else:
        transactions = crud.fund_user_ledger.get_multi_by_owner(
            db=db,
            owner_id=current_user.id,
            skip=skip,
            limit=limit
        )
    return transactions


@router.get("/{fund_id}", response_model=List[schemas.FundUserLedger])
def read_transactions_by_fund(
    fund_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve fund user ledger transactions.
    """
    transactions = crud.fund_user_ledger.get_multi_by_fund_owner(
        db=db,
        user_id=current_user.id,
        fund_id=fund_id,
        skip=skip,
        limit=limit
    )
    return transactions


@router.post("/{fund_id}", response_model=schemas.FundUserLedger)
def create_transaction(
    *,
    fund_id: int,
    db: Session = Depends(deps.get_db),
    transaction_in: schemas.UserLedgerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new fund user ledger transaction.
    """
    transaction = crud.fund_user_ledger.create_with_owner(
        db=db,
        obj_in=transaction_in,
        owner_id=current_user.id,
        fund_id=fund_id
    )
    return transaction


@router.get("/{transaction_id}", response_model=schemas.UserLedger)
def read_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    transaction = crud.user_ledger.get(db=db, id=transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if not crud.user.is_superuser(current_user) and (transaction.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return transaction
