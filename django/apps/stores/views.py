from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Product, Store
from .serializers import (
    ProductSerializer,
    PostProductSerializer,
    PutProductSerializer,

    StoreSerializer,
    PostStoreSerializer,
    PutStoreSerializer
)


def get_stores() -> Response:
    serialized = StoreSerializer(Store.objects.all(), many=True).data
    return Response(serialized, status=status.HTTP_200_OK)


def post_store(request: Request) -> Response:
    store = PostStoreSerializer(data=request.data)
    if not store.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response({'id': store.create().id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def stores(request: Request) -> Response:
    if request.method == 'GET':
        return get_stores()
    if request.method == 'POST':
        return post_store(request)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def delete_store(id: UUID) -> Response:
    try:
        Store.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


def get_store(id: UUID) -> Response:
    try:
        store = Store.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serialized = StoreSerializer(store).data
    return Response(serialized, status=status.HTTP_200_OK)


def put_store(request: Request, id: UUID) -> Response:
    store = PutProductSerializer(data=request.data)
    if not store.valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        existed = Store.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized = StoreSerializer(existed).data
    deserialized = StoreSerializer(data=serialized | store.data)
    deserialized.save()

    return Response(serialized, status=status.HTTP_200_OK)


@api_view(['DELETE', 'GET', 'PUT'])
def store(request: Request, id: UUID) -> Response:
    if request.method == 'DELETE':
        return delete_store(id)
    if request.method == 'GET':
        return get_store(id)
    if request.method == 'PUT':
        return put_store(request, id)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_products(store: UUID) -> Response:
    products = Product.objects.filter(store=store)
    serialized = ProductSerializer(products, many=True).data
    return Response(serialized, status=status.HTTP_200_OK)


def post_product(request, store: UUID) -> Response:
    product = PostProductSerializer(data=request.data)
    if not product.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        store = Store.objects.get(id=store)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    product = Product(store=store.id, **product.data)
    product.save()
    
    return Response({'id': product.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def products(request: Request, store: UUID) -> Response:
    if request.method == 'GET':
        return get_products(store)
    if request.method == 'POST':
        return post_product(request, store)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def delete_product(id: UUID) -> Response:
    try:
        Product.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


def get_product(id: UUID) -> Response:
    try:
        product = Product.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serialized = ProductSerializer(product).data
    return Response(serialized, status=status.HTTP_200_OK)


def put_product(request: Request, id: UUID) -> Response:
    product = PutProductSerializer(data=request.data)
    if not product.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        existed = Product.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized = ProductSerializer(existed).data
    deserialized = ProductSerializer(data=serialized | product.data)
    deserialized.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', 'GET', 'PUT'])
def product(request: Request, _: UUID, id: UUID) -> Response:
    if request.method == 'DELETE':
        return delete_product(id)
    if request.method == 'GET':
        return get_product(id)
    if request.method == 'PUT':
        return put_product(request, id)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
