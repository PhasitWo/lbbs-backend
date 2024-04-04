from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .student import Student
import random

# mockup = [
#     Student(1, "john", 1234)
# ]

# def searchStudent(name):
#     for std in mockup:
#         if std.name == name:
#             return std
#     return None

# print(searchStudent("john"))


@api_view(["POST"])
def login(request):
    return Response({"message": "test"})


@api_view(["GET"])
def test(request, arg=None):
    return Response({"message": arg})
