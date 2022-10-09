from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Product, Store


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        read_only_fields = ['id', 'store']


class StoreSerializer(ModelSerializer):
    class Meta:
        model = Store
        read_only_fields = ['id']


class PostStoreSerializer(ModelSerializer):
    class Meta:
        model = Store
        exclude = ['id']


PutStoreSerializer = PostStoreSerializer


class PostProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['id', 'store']


PutProductSerializer = PostProductSerializer
