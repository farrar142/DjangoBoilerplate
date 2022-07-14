import math
from functools import wraps
from django.db.models import *
from base.serializer import *


def get_int_num_from_kwargs(kwargs: dict, key: str, default_num=0):
    page = kwargs.get(key)
    if isinstance(page, str):
        return int(page)
    elif isinstance(page, int):
        return page
    else:
        return default_num


def pagination(func=None, offset=1, limit=10):
    def decorator(cb):
        @wraps(cb)
        def wrapper(qs: QuerySet, *args, **kwargs):
            page = get_int_num_from_kwargs(kwargs, "page", default_num=offset)
            perPage = get_int_num_from_kwargs(
                kwargs, "perPage", default_num=limit)
            paginated_qs = qs[(page-1)*perPage:page*perPage]
            result: QuerySet = cb(paginated_qs, *args, **kwargs)
            qs_len = 0
            try:
                qs_len = qs.count()
            except:
                qs_len = len(qs)
            current_len = 0
            try:
                current_len = result.count()
            except:
                current_len = len(result)
            length = math.ceil(qs_len/perPage)
            return {
                "type": "paginated",
                "contentLength": qs_len,
                "currentLength": len(result),
                "maxPage": length,
                "curPage": page,
                "perPage": perPage,
                "hasNext": page < length,
                "results": converter(result),
            }
        return wrapper
    return decorator(func) if callable(func) else decorator
