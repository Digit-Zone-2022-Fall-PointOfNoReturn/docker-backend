from rest_framework.serializers import ModelSerializer

from .models import Cart, Group, GroupMember


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['id']


class PostGroupsSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['id']


PutGroupsSerializer = PostGroupsSerializer


class GroupMemberSerializer(ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'
        read_only_fields = ['group', 'user']


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['group', 'user', 'store', 'product']
