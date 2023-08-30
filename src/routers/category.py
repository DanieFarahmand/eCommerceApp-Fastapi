from fastapi import APIRouter, Depends

from src.core.db.database import AsyncSession, get_session
from src.controlllers.user import admin_access
from src.schemas._in.category import CategoryCreateIn, DeleteCategoryIn
from src.controlllers.category import CategoryController
from src.dependencies.auth_dependenies import get_current_user

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/create/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def create_category(
        category_data: CategoryCreateIn,
        db_session: AsyncSession = Depends(get_session)):
    new_category = await CategoryController(db_session=db_session).create_category(
        category_data=category_data,
    )
    return {"message": f"Category [{new_category.name}] is created."}


@router.delete("/delete/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def delete_category(
        category_id: DeleteCategoryIn,
        db_session: AsyncSession = Depends(get_session)):
    await CategoryController(db_session=db_session).delete_category(category_id=category_id.id)
    return {"message": "category deleted."}


@router.get("/get/")
async def get_all_categories(db_session: AsyncSession = Depends(get_session)):
    categories = await CategoryController(db_session=db_session).get_all_category()
    return categories


@router.get("/{category_id}/")
async def get_category_products(
        category_id: int,
        db_session: AsyncSession = Depends(get_session)):
    products = await CategoryController(db_session=db_session).get_category_products(category_id=category_id)
    return products
