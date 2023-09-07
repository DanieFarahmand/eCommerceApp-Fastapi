from fastapi import Depends, HTTPException

from src.dependencies.auth_dependenies import get_current_user_from_db
from src.models.user import User


async def admin_access(user: User = Depends(get_current_user_from_db)):
    print(user.role.name)
    if user.role.name != "admin":
        raise HTTPException(403, "Forbidden")


async def customer_access(user: User):
    if user.role.name != "customer":
        raise HTTPException(403, "Forbidden")
