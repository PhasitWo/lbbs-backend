from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import ZODB
from .zodb.module.bookCatalog import BookCatalog

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root

@api_view(["POST"])
def login(request):
    return Response({"message": "test"})


@api_view(["GET"])
def test(request, id=None):
    print(BookCatalog)
    return Response({"message": "Hi"})
