import json
from datetime import datetime

from src.schemas.out.category import ProductsOut
from src.schemas.out.comment import CommentOut
from src.schemas.out.product import ProductOut, ProductCommentsOut
from src.schemas.out.user import UsersOut, UserOut


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        return super().default(obj)


def custom_json_dump(obj) -> str:
    return json.dumps(obj, cls=DateTimeEncoder)


def custom_json_load(json_str) -> json:
    return json.loads(json_str)


def serialize_products_from_redis(products):
    products_list = [ProductOut.parse_obj(product) for product in products]
    return ProductsOut(products_list=products_list)


def serialize_products(products):
    products_list = [ProductOut.from_orm(product) for product in products]
    return ProductsOut(products_list=products_list)


def serialize_comments(comments):
    comment_list = [CommentOut.from_orm(comment) for comment in comments]
    return ProductCommentsOut(products_list=comment_list)


def serialize_users(users):
    user_list = [UserOut.from_orm(user) for user in users]
    return UsersOut(products_list=user_list)
