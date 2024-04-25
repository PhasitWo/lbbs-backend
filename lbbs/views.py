from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .zodb.module.librarian import Librarian
from .zodb.module.bookCatalog import BookCatalog
from .zodb.module.book import Book
from .zodb.module.borrowing import Borrowing
from .zodb.module.constant import BorrowStatus
from .zodb.module.member import Member
import jwt
from functools import wraps
import ZODB
import transaction

transaction_manager = transaction.TransactionManager()
db = ZODB.DB("lbbs/zodb/db.fs")
connection = db.open(transaction_manager)
root = connection.root


def authenticate(permission_classes: list):
    def inner(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            header_token = request.headers.get("Authorization")
            # check if token exists
            if not header_token:
                return Response(
                    {"error": "no token"}, status=status.HTTP_401_UNAUTHORIZED
                )
            token = header_token.split(" ")[1]
            # check if token expired
            try:
                token_payload = jwt.decode(
                    token, "sample_secret_key", algorithms="HS256"
                )
            except jwt.ExpiredSignatureError:
                return Response(
                    {"error": "token expired"}, status=status.HTTP_401_UNAUTHORIZED
                )
            # check token permission
            if token_payload["permission"] not in permission_classes:
                return Response(
                    {"error": f"no permission, only {permission_classes} allowed"}, status=status.HTTP_401_UNAUTHORIZED
                )
            return func(request, token_payload, *args, **kwargs)
        return wrapper
    return inner


@api_view(["GET"])
@authenticate(["member", "librarian"])
def test(request, token_payload):
    print(token_payload)
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def member_login(request):
    username = request.data["username"]
    password = request.data["password"]
    is_admin = False
    user_id, user_name, token = Member.authenticate(root, username, password)
    if user_id == None:
        is_admin = True
        user_id, user_name, token = Librarian.authenticate(root, username, password)
    if not token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response({"user_name" : user_name, "user_id": user_id, "is_admin": is_admin,"access_token": token}, status=status.HTTP_200_OK)


# @authenticate
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
        else:
            res.update({"unique_id": None, "expected_date": None})
        unique_lst = list(catalog.get_book_list().values())
        unique_lst = [u.get_book_data()["unique_id"] for u in unique_lst]
        print(unique_lst)
        res.update(
            {
                "available": catalog.is_available(),
                "docs" : unique_lst
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
                "unique_id": data["book"].get_book_data()["unique_id"],
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
                "due_date": (
                    data["due_date"].strftime("%d/%m/%Y") if data["due_date"] else None
                ),
                "return_date": (
                    data["return_date"].strftime("%d/%m/%Y")
                    if data["return_date"]
                    else None
                ),
                "borrow_status": data["status"].value if data["status"] else None,
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
        if catalog.get_book_list().get(unique_id):
            target_catalog = catalog
            break
    if not target_catalog:
        return Response(
            {"error": "this book not belong to any catalog"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    new_id = root.borrowing.maxKey() + 1 if len(root.borrowing) else 0
    new_borrowing = Borrowing(new_id, member, target_catalog, book)
    completed = new_borrowing.start_borrow()
    if not completed:
        transaction_manager.abort()
        return Response(
            {"error": "this book is not available for borrowing"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    root.borrowing.insert(new_id, new_borrowing)
    transaction_manager.commit()
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
        transaction_manager.commit()
    elif s == "return":
        if current_status != "borrow":
            return Response(
                {"error": "current status is not 'borrow'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.return_book()
        transaction_manager.commit()
    elif s == "cancel":
        if current_status != "reserve":
            return Response(
                {"error": "current status is not 'reserve'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.cancel_reserve()
        transaction_manager.commit()
    else:
        return Response({"error": "invalid status"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def edit_book_catalog(request):
    book_id = request.data["book_id"]
    catalog: BookCatalog = root.bookCatalog.get(book_id)
    if not catalog:
        return Response(
            {"error": "no book catalog found"}, status=status.HTTP_400_BAD_REQUEST
        )
    catalog.edit(
        request.data["title"],
        request.data["genre"],
        request.data["author"],
        request.data["detail"],
    )
    transaction_manager.commit()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def add_book_catalog(request):
    book_id = request.data["book_id"]
    title = request.data["title"]
    if not title or title == "":
        return Response({"error": "no book title"}, status=status.HTTP_400_BAD_REQUEST)
    if book_id != None:
        if root.bookCatalog.has_key(book_id):
            return Response(
                {"error": "duplicate id"}, status=status.HTTP_400_BAD_REQUEST
            )
        new_id = book_id
    else:
        new_id = root.bookCatalog.maxKey() + 1 if len(root.bookCatalog) else 0
    new_book_catalog = BookCatalog(
        new_id,
        title,
        request.data["genre"],
        request.data["author"],
        request.data["detail"],
        request.data["coverUrl"],
    )
    root.bookCatalog.insert(new_id, new_book_catalog)
    transaction_manager.commit()
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST", "GET"])
def add_book(request):
    book_id = request.data["book_id"]
    unique_id = request.data["unique_id"]
    catalog: BookCatalog = root.bookCatalog.get(book_id)
    if not catalog:
        return Response(
            {"error": "no book catalog found"}, status=status.HTTP_400_BAD_REQUEST
        )
    if unique_id != None:
        if root.book.has_key(unique_id):
            return Response(
                {"error": "duplicate unique_id"}, status=status.HTTP_400_BAD_REQUEST
            )
        new_id = unique_id
    else:
        new_id = root.book.maxKey() + 1 if len(root.bookCatalog) else 0
    new_book = Book(new_id)
    catalog.add_book_by_object(new_book)
    root.book.insert(new_id, new_book)
    transaction_manager.commit()
    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authenticate(["member"])
def get_member_data(request, token_payload):
    member_id = token_payload["member_id"]
    member = root.member.get(member_id)
    if not member:
        return Response(
            {"error": "no member found"}, status=status.HTTP_400_BAD_REQUEST
        )
    lst = member.get_borrow_list()
    borrow_count = 0
    reserve_count = 0
    fine = 0
    for borrowing in lst:
        status = borrowing.get_borrow_detail()["status"]
        fine += borrowing.get_borrow_detail()["fine"]
        if status == BorrowStatus.BORROW:
            borrow_count += 1
        elif status == BorrowStatus.RESERVE:
            reserve_count += 1
    return Response(
        {"borrow_count": borrow_count, "reserve_count": reserve_count, "fine": fine}
    )

# FIXME require auth
@api_view(["GET"])
@authenticate(["member"])
def get_member_borrowing(request, token_payload):
    member_id = token_payload["member_id"]
    member = root.member.get(member_id)
    if not member:
        return Response(
            {"error": "no member found"}, status=status.HTTP_400_BAD_REQUEST
        )
    res = []
    lst = member.get_borrow_list()
    for borrowing in lst:
        data = borrowing.get_borrow_detail()
        res.append(
            {
                "borrow_id": data["borrow_id"],
                "member_id": data["member"].get_id(),
                "unique_id": data["book"].get_book_data()["unique_id"],
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
                "due_date": (
                    data["due_date"].strftime("%d/%m/%Y") if data["due_date"] else None
                ),
                "return_date": (
                    data["return_date"].strftime("%d/%m/%Y")
                    if data["return_date"]
                    else None
                ),
                "borrow_status": data["status"].value if data["status"] else None,
                "fine": data["fine"],
            }
        )
    return Response({"borrowing_list": res})

# FIXME require auth
@api_view(["POST"])
def create_reserve_borrowing(request):
    member_id = request.data["member_id"]
    unique_id = request.data["unique_id"]
    member = root.member.get(member_id)
    if not member:
        return Response(
            {"error": "no member found"}, status=status.HTTP_400_BAD_REQUEST
        )
    # check if this member is borrowing this book
    lst = member.get_borrow_list()
    for borrowing in lst:
        data = borrowing.get_borrow_detail()
        if (
            data["status"] == BorrowStatus.BORROW
            and data["book"].get_book_data()["unique_id"] == unique_id
        ):
            return Response(
                {
                    "error": "this member is borrowing this book, reservation is not allowed"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    book = root.book.get(unique_id)
    if not book:
        return Response({"error": "no book found"}, status=status.HTTP_400_BAD_REQUEST)
    # can be optimized
    bookCatalogs = list(root.bookCatalog.values())
    target_catalog = None
    for catalog in bookCatalogs:
        if catalog.get_book_list().get(unique_id):
            target_catalog = catalog
            break
    if not target_catalog:
        return Response(
            {"error": "this book not belong to any catalog"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    new_id = root.borrowing.maxKey() + 1 if len(root.borrowing) else 0
    new_borrowing = Borrowing(new_id, member, target_catalog, book)
    completed = new_borrowing.start_reserve()
    if not completed:
        transaction_manager.abort()
        return Response(
            {"error": "cannot reserve this book"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    root.borrowing.insert(new_id, new_borrowing)
    transaction_manager.commit()
    return Response(status=status.HTTP_201_CREATED)
