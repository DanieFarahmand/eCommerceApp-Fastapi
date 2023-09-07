from fastapi import APIRouter, Depends

from src.core.db.database import AsyncSession, get_session
from src.dependencies.user_dependencies import admin_access
from src.schemas._in.category import CategoryCreateIn, DeleteCategoryIn
from src.schemas.out.category import ProductsForCategoryOut
from src.schemas.out.product import ProductOut
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


@router.get("/all/")
async def get_all_categories(db_session: AsyncSession = Depends(get_session)):
    categories = await CategoryController(db_session=db_session).get_all_category()
    return categories


@router.get("/{category_id}/", response_model=ProductsForCategoryOut)
async def get_products_for_category(
        category_id: int,
        db_session: AsyncSession = Depends(get_session)):
    products = await CategoryController(db_session=db_session).get_category_products(category_id=category_id)
    print(products)
    product_out_list = [ProductOut.from_orm(product) for product in products]
    return ProductsForCategoryOut(products_list=product_out_list)
