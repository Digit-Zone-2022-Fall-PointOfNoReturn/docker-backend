from rest_framework.serializers import ModelSerializer

from .models import Cart, Group, GroupMember


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        read_only_fields = ['id']


class PostGroupsSerializer(ModelSerializer):
    class Meta:
        model = Group
        exclude = ['id']


PutGroupsSerializer = PostGroupsSerializer


class GroupMemberSerializer(ModelSerializer):
    class Meta:
        model = GroupMember
        read_only_fields = ['group', 'user']


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        read_only_fields = ['group', 'user', 'store', 'product']
