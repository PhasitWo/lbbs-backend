from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .zodb.module.bookCatalog import BookCatalog
import ZODB

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root


# def my_decor(func: function):
#     def wrapper(*args, **kwargs):
#         request = args[0]
#         if not request.query_params.get("title"):
#             Response(status=status.HTTP_400_BAD_REQUEST)
#         return func(*args, **kwargs)

#     return wrapper


# @my_decor
@api_view(["GET"])
def get_book(request):
    q = request.query_params.get("title")
    if not q:
        bookCatalogs = list(root.bookCatalog.values())
    else:
        bookCatalogs = BookCatalog.search_book_catalog(root, q)
    lst = []
    for catalog in bookCatalogs:
        catalog_data = catalog.get_book_data()
        data = {
            "book_id": catalog_data["book_id"],
            "title": catalog_data["title"],
            "genre": catalog_data["genre"],
            "author": [catalog_data["author"]],
            "cover": catalog_data["cover"],
        }
        lst.append(data)
    return Response({"docs": lst})


@api_view(["GET"])
def get_book_detail(request, id=None):
    catalog = root.bookCatalog.get(id)
    if catalog:
        res: dict = catalog.get_book_data()
        for_reserve = catalog.get_available_for_reserve()
        if for_reserve:
            res.update(
                {
                    "unique_id": for_reserve.get_book_data()["unique_id"],
                    "expected_date": for_reserve.get_book_data()[
                        "expected_date"
                    ].strftime("%d/%m/%Y"),
                }
            )
        res.update(
            {
                "available": catalog.is_available(),
            }
        )
        return Response(res)
    return Response(status=status.HTTP_204_NO_CONTENT)

def get_borrowing(request):
    q = request.query_params.get("id")
    if not q:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    