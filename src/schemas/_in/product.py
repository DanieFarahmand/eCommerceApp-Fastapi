from typing import Dict

from pydantic import BaseModel, conint, validator


class ProductCreateIn(BaseModel):
    title: str
    description: str
    price: int
    attributes: Dict
    category_id: int
    sold_amount: int = 0

    class Config:
        arbitrary_types_allowed = True


class ProductIn(BaseModel):
    id: int


class RateProductIn(BaseModel):
    rate: conint(ge=1, le=5)

    @validator('rate')
    def validate_rate(cls, rate):
        if rate < 1 or rate > 5:
            raise ValueError("Rate must be between 1 and 5")
        return rate
