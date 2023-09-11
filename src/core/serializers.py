import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        return super().default(obj)


def custom_json_dump(obj) -> str:
    return json.dumps(obj, cls=DateTimeEncoder)


def custom_json_load(json_str) -> json:
    return json.loads(json_str)
