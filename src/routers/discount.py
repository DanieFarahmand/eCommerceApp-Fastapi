from fastapi import APIRouter, Depends, BackgroundTasks

from src.core.db.database import get_session, AsyncSession
from src.dependencies.auth_dependenies import get_current_user
from src.dependencies.user_dependencies import admin_access
from src.schemas._in.discount import DiscountIn, DiscountIdIn, CouponIn, CouponUseIn
from src.controlllers.discount import DiscountController, CouponController

router = APIRouter(prefix="/discount", tags=["Discounts"])


@router.post("/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def put_discount(
        discount_data: DiscountIn,

        db_session: AsyncSession = Depends(get_session)):
    discount = await DiscountController(db_session=db_session).apply(
        discount_percent=discount_data.discount_percent,
        expiration_hours=discount_data.expiration_hours,
        product_id=discount_data.product_id,
    )

    return {"message": "Your comment added."}


@router.delete("/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def delete_discount(
        discount_id: DiscountIdIn,
        db_session: AsyncSession = Depends(get_session)):
    await DiscountController(db_session=db_session).delete(
        discount_id=discount_id.id
    )


@router.delete("/delete/all", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def delete_all_discounts(db_session: AsyncSession = Depends(get_session)):
    await DiscountController(db_session=db_session).delete_all_discounts()


@router.post("/coupon/generate/", dependencies=[Depends(get_current_user), Depends(admin_access)])
async def generate_discount_coupon(
        coupon_data: CouponIn,
        db_session: AsyncSession = Depends(get_session)):
    coupon_code = await CouponController(db_session=db_session).generate_coupon(
        code_name=coupon_data.code_name,
        discount_percent=coupon_data.discount_percent,
        expiration_hours=coupon_data.expiration_hours
    )
    return coupon_code


@router.post("/coupon/use/")
async def use_coupon(
        coupon_data: CouponUseIn,
        db_session: AsyncSession = Depends(get_session)):
    new_price = await CouponController(db_session=db_session).use_coupon(
        code=coupon_data.code_name,
        total_price=coupon_data.total_price

    )
    return new_price
