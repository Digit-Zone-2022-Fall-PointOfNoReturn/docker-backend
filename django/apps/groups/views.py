from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import Telegram
from stores.models import Store

from .models import Cart, Group, GroupMember
from .serializers import (
    CartSerializer,
    
    GroupSerializer,
    PostGroupsSerializer,
    PutGroupsSerializer,

    GroupMemberSerializer
)


def get_groups(request: Request) -> Response:
    if 'user' not in request.query_params:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    groups = GroupMember.objects.filter(user=request.query_params['user'])
    serialized = GroupMemberSerializer(groups, many=True).data
    return Response(serialized, status=status.HTTP_200_OK)


def post_group(request: Request) -> Response:
    if 'users' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    group = PostGroupsSerializer(data=request.data)
    if not group.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    users = request.data['users'] + [request.data['admin']]
    
    try:
        for user in users:
            Telegram.objects.get(id=user)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    created = group.create(group.validated_data)
    for user in users:
        GroupMember(group=created, user=Telegram.objects.get(id=user)).save()
    return Response({ "id": created.id }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def groups(request: Request) -> Response:
    if request.method == 'GET':
        return get_groups(request)
    if request.method == 'POST':
        return post_group(request)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def delete_group(id: UUID) -> Response:
    try:
        Group.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


def get_group(id: UUID) -> Response:
    try:
        group = Group.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serialized = GroupSerializer(group).data
    return Response(serialized, status=status.HTTP_200_OK)


def put_group(request: Request, id: UUID) -> Response:
    if 'name' not in request.data and 'admin' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    try:
        group = Group.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if 'name' in request.data:
        group.name = request.data['name']  # Fall on wrong name?
    
    if 'admin' in request.data:
        try:
            admin = Telegram.objects.get(id=request.data['admin'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        group.admin = admin
    
    group.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', 'GET', 'PUT'])
def group(request: Request, id: UUID) -> Response:
    if request.method == 'DELETE':
        return delete_group(id)
    if request.method == 'GET':
        return get_group(id)
    if request.method == 'PUT':
        return put_group(request, id)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def delete_groupe_store(group_id: UUID, store_id: UUID) -> Response:
    try:
        group = Group.objects.get(id=group_id)
        Store.objects.get(id=store_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if group.collecting:
        return Response(status=status.HTTP_409_CONFLICT)
    
    group.store = None
    group.save()
    return Response(status=status.HTTP_200_OK)


def put_groupe_store(group_id: UUID, store_id: UUID) -> Response:
    try:
        group = Group.objects.get(id=group_id)
        store = Store.objects.get(id=store_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if group.collecting:
        return Response(status=status.HTTP_409_CONFLICT)
    
    group.store = store
    group.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', 'PUT'])
def group_store(request: Request, group: UUID, store: UUID) -> Response:
    if request.method == 'DELETE':
        return delete_groupe_store(group, store)
    if request.method == 'PUT':
        return put_groupe_store(group, store)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def group_store_carts(request: Request, group_id: UUID, store_id: UUID) -> Response:
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    try:
        group = Group.objects.get(id=group_id)
        store = Store.objects.get(id=store_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    carts = Cart.objects.filter(group=group.id, store=store.id)
    serialized = CartSerializer(carts, many=True).data
    return Response(serialized, status=status.HTTP_200_OK)


@api_view(['POST'])
def group_collecting_drop(request: Request, group_id: UUID) -> Response:
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if group.store is None:
        return Response(status=status.HTTP_409_CONFLICT)

    if group.collecting:
        return Response(status=status.HTTP_409_CONFLICT)

    Cart.objects.filter(group=group.id, store=group.store).delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def group_collecting_start(request: Request, group_id: UUID) -> Response:
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if group.store is None:
        return Response(status=status.HTTP_409_CONFLICT)

    group.collecting = True
    group.save()
    
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def group_collecting_stop(request: Request, group_id: UUID) -> Response:
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if group.store is None:
        return Response(status=status.HTTP_409_CONFLICT)

    group.collecting = False
    group.save()
    
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def group_users(request: Request, group_id: UUID) -> Response:
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    users = GroupMember.objects.filter(group=group.id)
    serialized = GroupMemberSerializer(users, many=True).data
    return Response(serialized, status=status.HTTP_200_OK)


def delete_user(group: UUID, user: int) -> Response:
    try:
        GroupMember.objects.get(group=group, user=user).delete()
        Cart.objects.filter(group=group, user=user).delete()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)
    

def post_user(group: UUID, user: int) -> Response:
    try:
        Group.objects.get(id=group)
        Telegram.objects.get(id=user)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    GroupMember(group=group, user=user)
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', 'POST'])
def group_user(request: Request, group: UUID, user: int) -> Response:
    if request.method == 'DELETE':
        return delete_user(group, user)
    if request.method == 'POST':
        return post_user(group, user)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def delete_user_cart(group: UUID, user: int, store: UUID) -> Response:
    Cart.objects.filter(group=group, user=user, store=store).delete()
    return Response(status=status.HTTP_200_OK)


def get_user_cart(group: UUID, user: int, store: UUID) -> Response:
    carts = Cart.objects.filter(group=group, user=user, store=store)
    serialized = CartSerializer(carts, many=True).data
    return Response(serialized, status=status.HTTP_200_OK)


@api_view(['DELETE', 'GET'])
def user_cart(request: Request, group: UUID, user: int, store: UUID) -> Response:
    if request.method == 'DELETE':
        return delete_user_cart(group, user, store)
    if request.method == 'GET':
        return get_user_cart(group, user, store)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def cart_product_change(group_id: UUID, user_id: int, store_id: UUID, product_id: UUID, delta: int) -> Response:
    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if not group.collecting:
        return Response(status=status.HTTP_409_CONFLICT)
    
    if group.store.id != store_id:
        return Response(status=status.HTTP_400_CONFLICT)

    try:
        product = Cart.objects.get(group=group, user=user_id, store=store_id, product=product)
    except ObjectDoesNotExist:
        if delta <= 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product = Cart(group=group, user=user_id, store=store_id, product=product, amount=delta)
        product.save()
        
        return Response(status=status.HTTP_200_OK)
    
    amount = product.amount + delta
    if amount <= 0:
        product.delete()
        return Response(status=status.HTTP_200_OK)

    product.amount = amount
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', 'PUT'])
def cart_product(request: Request, group: UUID, user: int, store: UUID, product: UUID) -> Response:
    amount = request.data.get('amount', 1)

    if request.method == 'DELETE':
        return cart_product_change(group, user, store, product, -abs(amount))
    if request.method == 'PUT':
        return cart_product_change(group, user, store, product, abs(amount))
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
