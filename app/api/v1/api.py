from fastapi import APIRouter

from app.api.v1.endpoints import funds, login, users, user_ledgers, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(funds.router, prefix="/funds", tags=["Funds"])
api_router.include_router(user_ledgers.router, prefix="/user-ledgers", tags=["User Ledgers"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utils"])
