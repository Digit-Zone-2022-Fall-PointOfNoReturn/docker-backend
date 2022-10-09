from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Telegram


def delete_user(id: int) -> Response:
    try:
        user = Telegram.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_200_OK)


def post_user(id: int) -> Response:
    try:
        Telegram.objects.get(id=id)
        return Response(status=status.HTTP_409_CONFLICT)
    except ObjectDoesNotExist:
        pass
    
    user = Telegram.objects.create(id=id)
    user.save()
    
    return Response(status=status.HTTP_201_CREATED)


@api_view(['DELETE', 'POST'])
def user(request: Request, id: int) -> Response:
    if request.method == 'DELETE':
        return delete_user(id)
    if request.method == 'POST':
        return post_user(id)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
