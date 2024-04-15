from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .zodb.module.bookCatalog import BookCatalog
from .zodb.module.borrowing import Borrowing
import ZODB
import transaction

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


@api_view(["GET"])
def get_borrowing(request):
    q = request.query_params.get("id")
    if not q:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    lst = []
    result = Borrowing.search_borrowing(root, int(q))
    for borrowing in result:
        data = borrowing.get_borrow_detail()
        lst.append(
            {
                "borrow_id": data["borrow_id"],
                "member_id": data["member"].get_id(),
                "book_title": data["book_catalog"].get_book_data()["title"],
                "reserve_date": (
                    data["reserve_date"].strftime("%d/%m/%Y")
                    if data["reserve_date"]
                    else None
                ),
                "expected_date": (
                    data["expected_date"].strftime("%d/%m/%Y")
                    if data["expected_date"]
                    else None
                ),
                "borrow_date": (
                    data["borrow_date"].strftime("%d/%m/%Y")
                    if data["borrow_date"]
                    else None
                ),
                "borrow_status": data["status"],
                "fine": data["fine"],
            }
        )
    return Response({"borrowing_list": lst})


@api_view(["POST"])
def create_borrowing(request):
    member_id = request.data["member_id"]
    unique_id = request.data["unique_id"]
    member = root.member.get(member_id)
    if not member:
        return Response(
            {"error": "no member found"}, status=status.HTTP_400_BAD_REQUEST
        )
    book = root.book.get(unique_id)
    if not book:
        return Response({"error": "no book found"}, status=status.HTTP_400_BAD_REQUEST)
    # can be optimized
    bookCatalogs = list(root.bookCatalog.values())
    target_catalog = None
    for catalog in bookCatalogs:
        if bookCatalogs.get_book_list().get(unique_id):
            target_catalog = catalog
            break
    if not target_catalog:
        return Response({"error": "this book not belong to any catalog"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    new_id = root.borrowing.maxKey() if len(root.borrowing) else 0
    new_borrowing = Borrowing(new_id, member, target_catalog, book)
    root.borrowing.insert(new_id, new_borrowing)
    transaction.commit()
    return Response(status=status.HTTP_201_CREATED)

@api_view(["POST"])
def set_borrowing_status(request):
    borrow_id = request.data["borrow_id"]
    s = request.data["status"]
    borrowing = root.borrowing.get(borrow_id)
    if not borrowing:
        return Response(
            {"error": "no borrowing found"}, status=status.HTTP_400_BAD_REQUEST
        )
    current_status = borrowing.get_borrow_detail()["status"].value
    if s == "borrow":
        if current_status != "reserve":
            return Response(
                {"error": "current status is not 'reserve'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        completed = borrowing.start_borrow()
        if not completed:
            return Response(
                {"error": "This book is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        transaction.commit()
    elif s == "return":
        if current_status != "borrow":
            return Response(
                {"error": "current status is not 'borrow'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.return_book()
        transaction.commit()
    elif s == "cancel":
        if current_status != "reserve":
            return Response(
                {"error": "current status is not 'reserve'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.cancel_reserve()
        transaction.commit()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)
