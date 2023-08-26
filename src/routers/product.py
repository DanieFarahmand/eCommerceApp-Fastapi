from fastapi import APIRouter, Depends, HTTPException

from src.core.db.database import AsyncSession, get_session
from src.controlllers.user import AdminUser, admin_access
from src.schemas._in.product import ProductCreateIn, ProducDeleteIn
from src.models.product import Product
from src.dependencies.auth_dependenies import get_current_user

router = APIRouter(prefix="/product", tags=["Products"])


@router.post("/create/",
             # dependencies=[Depends(admin_access)]
             )
async def create_product(
        product_data: ProductCreateIn,
        # user_id: str = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_session)):
    new_product = await Product().create_product(
        product_data=product_data,
        session=db_session,

    )
    return {"message": f"Product [{new_product.title}] is created ."}


@router.get("/get-all-products/")
async def get_all_products(db_session: AsyncSession = Depends(get_session)):
    products = await Product().get_all_products(session=db_session)
    return products


@router.delete("/delete/")
async def get_all_products(
        product_id: ProducDeleteIn,
        db_session: AsyncSession = Depends(get_session)):
    products = await Product().delete_product(session=db_session, product_id=product_id.id)
    return {"message": "product deleted."}
