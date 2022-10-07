from uuid import UUID, uuid4

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Telegram
from .serializers import TelegramSerializer


def delete_user(id: UUID) -> Response:
    try:
        user = Telegram.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_200_OK)


def put_user(request: Request, id: UUID) -> Response:
    # Safe, other keys ignored
    if not request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Telegram.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized = TelegramSerializer(instance=user)
    deserialized = TelegramSerializer(data=request.data | serialized.data)
    if not deserialized.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    deserialized.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', 'PUT'])
def user(request: Request, id: UUID) -> Response:
    if request.method == 'DELETE':
        return delete_user(id)
    if request.method == 'PUT':
        return put_user(request, id)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_user(request: Request) -> Response:
    if 'tag' in request.query_params:
        try:
            user = Telegram.objects.get(tag=request.query_params['tag'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serialized = TelegramSerializer(user).data
        return Response(serialized)

    if 'name' in request.query_params:
        users = Telegram.objects.filter(name=request.query_params['name'])
        return Response(TelegramSerializer(users, many=True).data)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def post_user(request: Request) -> Response:
    if 'name' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if 'tag' in request.data:
        try:
            Telegram.objects.get(tag=request.data['tag'])
            return Response(status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            pass
    
    user = Telegram.objects.create(name=request.data['name'], tag=request.data.get('tag', f"-{uuid4()}"))
    user.save()
    
    return Response({"id": user.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def users(request: Request) -> Response:
    if request.method == 'GET':
        return get_user(request)
    if request.method == 'POST':
        return post_user(request)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
