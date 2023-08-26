from fastapi import APIRouter, Depends, HTTPException

from src.core.db.database import AsyncSession, get_session
from src.controlllers.user import AdminUser, admin_access
from src.schemas._in.user import ChangeRoleIn

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/get-all-users/", dependencies=[Depends(admin_access)])
async def get_all_users(db_session: AsyncSession = Depends(get_session)):
    users = await AdminUser().get_all_users(db_session=db_session)
    return users


@router.get("/get-user-by-id/")
async def get_user_by_id(user_id: int, db_session: AsyncSession = Depends(get_session)):
    try:
        user = await AdminUser().get_user_by_id(db_session=db_session, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User with this id does not exist.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    return user.email


@router.put("change-user-role")
async def change_user_role(role: ChangeRoleIn, user_id: int, db_session: AsyncSession = Depends(get_session)):
    await AdminUser().change_user_role(
        db_session=db_session,
        user_id=user_id,
        role=role.role
    )
    return {"message": f"user became {role.role.name}."}


@router.delete("/delete/")
async def delete_user(user_id: int, db_session: AsyncSession = Depends(get_session)):
    await AdminUser().delete_user(user_id=user_id, db_session=db_session)
    return {"message": "User deleted."}
