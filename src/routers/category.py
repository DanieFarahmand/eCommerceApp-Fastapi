from fastapi import APIRouter, Depends, HTTPException

from src.core.db.database import AsyncSession, get_session
from src.controlllers.user import AdminUser, admin_access
from src.schemas._in.category import CategoryCreateIn, DeleteCategoryIn
from src.models.category import Category
from src.dependencies.auth_dependenies import get_current_user, get_current_user_from_db

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/create/")
async def create_category(
        category_data: CategoryCreateIn,
        # user_id: str = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_session)):
    new_category = await Category().create_category(
        session=db_session,
        category_data=category_data,
    )
    return {"message": f"Product [{new_category.name}] is created ."}


@router.delete("/delete/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def delete_category(
        category_id: DeleteCategoryIn,
        db_session: AsyncSession = Depends(get_session)):
    await Category.delete_category(session=db_session, category_id=category_id.id)
    return {"message": "category deleted."}


@router.get("/get/")
async def get_all_categories(db_session: AsyncSession = Depends(get_session)):
    categories = await Category.get_all_category(session=db_session)
    return categories
