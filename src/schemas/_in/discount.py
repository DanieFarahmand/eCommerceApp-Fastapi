from pydantic import BaseModel, Field


class DiscountIn(BaseModel):
    discount_percent: int
    expiration_hours: int
    product_id: int

    class Config:
        orm_mode = True


class DiscountIdIn(BaseModel):
    id: int


class CouponIn(BaseModel):
    discount_percent: int
    expiration_hours: int
    code_name: str = Field(min_length=5)

    class Config:
        orm_mode = True


class CouponUseIn(BaseModel):
    code_name: str = Field(min_length=5)
    total_price: int

    class Config:
        orm_mode = True
