from django.http import HttpRequest
from ninja import NinjaAPI
api = NinjaAPI(csrf=False)


@api.get('test')
def test(request: HttpRequest):
    return "true"
