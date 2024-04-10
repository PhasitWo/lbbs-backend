from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import ZODB

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root

@api_view(["POST"])
def login(request):
    return Response({"message": "test"})


@api_view(["GET"])
def test(request, id=None):
    m = root.member.get(id)
    res = m.__str__() if m else None
    return Response({"message": res})
