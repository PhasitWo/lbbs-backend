from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
import ZODB

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root

@api_view(["POST"])
def login(request):
    return Response({"message": "test"})


@api_view(["GET"])
def test(request, id=None):
    print(root.book.get(123).get_book_data()["status"].value)
    return Response({"message": "Hi"})

@api_view(["GET"])
def get_book_catalog(request, id=None):
    catalog = root.bookCatalog.get(id)
    if catalog:
        return Response(catalog.get_book_data())
    return Response(status=status.HTTP_204_NO_CONTENT)
