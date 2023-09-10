from fastapi import APIRouter, Depends, HTTPException

from src.controlllers.user import UserController
from src.core.db.database import AsyncSession, get_session
from src.dependencies.user_dependencies import admin_access
from src.dependencies.auth_dependenies import get_current_user
from src.schemas._in.user import ChangeRoleIn, UserIdIn
from src.schemas.out.user import UserOut, UsersOut
from src.core.serializers import serialize_users

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/all/", response_model=UsersOut, dependencies=[Depends(get_current_user), Depends(admin_access)])
async def get_all_users(db_session: AsyncSession = Depends(get_session)):
    users = await UserController(db_session=db_session).get_all_users()
    return serialize_users(users)


@router.get("/get-user-by-id/", response_model=UserOut, dependencies=[Depends(get_current_user), Depends(admin_access)])
async def get_user_by_id(user_id: UserIdIn, db_session: AsyncSession = Depends(get_session)):
    try:
        user = await UserController(db_session=db_session).get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User with this id does not exist.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    return UserOut.from_orm(user)


@router.put("change-user-role")
async def change_user_role(role: ChangeRoleIn, user_id: UserIdIn, db_session: AsyncSession = Depends(get_session)):
    await UserController(db_session=db_session).change_user_role(
        user_id=user_id.id,
        role=role.role)
    return {"message": f"user became {role.role.name}."}


@router.delete("/delete/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def delete_user(user_id: UserIdIn, db_session: AsyncSession = Depends(get_session)):
    await UserController(db_session=db_session).delete_user(user_id=user_id.id)
    return {"message": "User deleted."}
