from rest_framework import serializers
from .models import User, Parent, Child


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'language']
        read_only_fields = ['id', 'role']


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'name_ja', 'name_en', 'class_name', 'enrolled_at']


class ParentSerializer(serializers.ModelSerializer):
    children = ChildSerializer(many=True, read_only=True)

    class Meta:
        model = Parent
        fields = ['id', 'name_ja', 'name_en', 'phone', 'children']
