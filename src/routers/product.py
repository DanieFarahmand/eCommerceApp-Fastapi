from fastapi import APIRouter, Depends, HTTPException

from src.core.db.database import AsyncSession, get_session
from src.controlllers.user import admin_access
from src.schemas._in.product import ProductCreateIn, ProductDeleteIn
from src.controlllers.product import ProductController
from src.dependencies.auth_dependenies import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
async def create_product(product_data: ProductCreateIn, db_session: AsyncSession = Depends(get_session)):
    try:
        product = await ProductController(db_session=db_session).create_product(product_data=product_data)
        return {"message": f"Product [{product.title}] is created ."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/get-all-products/")
async def get_all_products(db_session: AsyncSession = Depends(get_session)):
    products = await ProductController(db_session=db_session).get_all_products()
    return products


@router.delete("/delete/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def delete_product(
        product_id: ProductDeleteIn,
        db_session: AsyncSession = Depends(get_session)):
    products = await ProductController(db_session=db_session).delete_product(product_id=product_id.id)
    return {"message": "product deleted."}


@router.get("/{product_id}/")
async def get_product(product_id: int, db_session: AsyncSession = Depends(get_session)):
    product = await ProductController(db_session=db_session).get_product(product_id=product_id)
    if product is None:
        return {"error": "Product not found"}
    return product
