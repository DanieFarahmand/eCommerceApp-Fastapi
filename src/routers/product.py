from fastapi import APIRouter, Response, Depends, HTTPException

from src.controlllers.category import CategoryController
from src.core.cache import CacheHandler
from src.core.db.database import AsyncSession, get_session
from src.core.redis import get_redis, RedisHandler
from src.dependencies.user_dependencies import admin_access
from src.schemas._in.product import ProductCreateIn, ProductDeleteIn
from src.schemas.out.category import ProductsOut
from src.schemas.out.product import ProductCommentsOut, ProductOut
from src.controlllers.product import ProductController
from src.dependencies.auth_dependenies import get_current_user
from src.core.serializers import serialize_products, serialize_products_from_redis, serialize_comments

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def create_product(product_data: ProductCreateIn, db_session: AsyncSession = Depends(get_session)):
    try:
        product = await ProductController(db_session=db_session).create_product(product_data=product_data)
        return {"message": f"Product [{product.title}] is created ."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/get-all-products/", response_model=ProductsOut)
async def get_all_products(db_session: AsyncSession = Depends(get_session)):
    products = await ProductController(db_session=db_session).get_all_products()
    return serialize_products(products)


@router.delete("/delete/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def delete_product(
        product_id: ProductDeleteIn,
        db_session: AsyncSession = Depends(get_session)):
    products = await ProductController(db_session=db_session).delete_product(product_id=product_id.id)
    return {"message": "product deleted."}


@router.get("/{product_id}/", response_model=ProductOut)
async def get_product(product_id: int, db_session: AsyncSession = Depends(get_session)):
    product = await ProductController(db_session=db_session).get_product(product_id=product_id)
    return ProductOut.from_orm(product)


@router.get("/{product_id}/comments", response_model=ProductCommentsOut)
async def get_comments_of_product(product_id: int, db_session: AsyncSession = Depends(get_session)):
    comments = await ProductController(db_session=db_session).get_comments(product_id=product_id)
    return serialize_comments(comments)


@router.get("/category/{category_id}", response_model=ProductsOut)
async def get_products_for_category(
        category_id: int,
        response: Response,
        redis_db: RedisHandler = Depends(get_redis),
        db_session: AsyncSession = Depends(get_session)
):
    products = await CategoryController(db_session=db_session).get_category_products(category_id=category_id)

    await CacheHandler(redis_db=redis_db).set_cached_data(
        name=f"product-{category_id}",
        value=[ProductOut.from_orm(product).dict() for product in products],
        exp=60
    )
    response.headers["Cache-Control"] = "public, max-age=60"
    response.headers["Expires"] = "3600"

    return serialize_products(products)


@router.get("/category/{category_id}/sort-by-price-cheap", response_model=ProductsOut)
async def sort_products_by_price_cheap(
        category_id: int,
        response: Response,
        redis_db: RedisHandler = Depends(get_redis)
):
    cached_data = await CacheHandler(redis_db=redis_db).get_cached_data(f"product-{category_id}")
    products = await ProductController.sort_by_price_cheap(products=cached_data)
    response.headers["X-Cache-Status"] = "HIT"

    return serialize_products_from_redis(products)


@router.get("/category/{category_id}/sort-by-price-expensive", response_model=ProductsOut)
async def sort_products_by_price_expansive(
        category_id: int,
        response: Response,
        redis_db: RedisHandler = Depends(get_redis)
):
    cached_data = await CacheHandler(redis_db=redis_db).get_cached_data(f"product-{category_id}")
    products = await ProductController.sort_by_price_expansive(products=cached_data)
    response.headers["X-Cache-Status"] = "HIT"

    return serialize_products_from_redis(products)


@router.get("/category/{category_id}/sort-by-bestselling", response_model=ProductsOut)
async def sort_products_by_bestselling(
        category_id: int,
        response: Response,
        redis_db: RedisHandler = Depends(get_redis)
):
    cached_data = await CacheHandler(redis_db=redis_db).get_cached_data(f"product-{category_id}")
    products = await ProductController.sort_by_bestselling(products=cached_data)
    response.headers["X-Cache-Status"] = "HIT"
    return serialize_products_from_redis(products)


@router.get("/category/{category_id}/sort-by-newest", response_model=ProductsOut)
async def sort_products_by_newest(
        category_id: int,
        response: Response,
        redis_db: RedisHandler = Depends(get_redis)
):
    cached_data = await CacheHandler(redis_db=redis_db).get_cached_data(f"product-{category_id}")
    products = await ProductController.sort_by_newest(products=cached_data)
    response.headers["X-Cache-Status"] = "HIT"

    return serialize_products_from_redis(products)


@router.get("/category/{category_id}/sort-by-rating", response_model=ProductsOut)
async def sort_products_by_rating(): ...


