from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Product, Store


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'store']


class StoreSerializer(ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['id']


class PostStoreSerializer(ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        exclude = ['id']


PutStoreSerializer = PostStoreSerializer


class PostProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['id', 'store']


PutProductSerializer = PostProductSerializer
