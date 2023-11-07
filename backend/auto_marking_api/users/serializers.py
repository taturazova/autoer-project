from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = ("username",)


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "auth_token",
        )
        read_only_fields = ("auth_token",)
        extra_kwargs = {"password": {"write_only": True}}


class WhoAmISerializer(serializers.Serializer):
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        return {
            "add_report": obj.is_staff,
            "associate": obj.is_staff,
            "edit_tags": obj.is_staff,
            "is_active": obj.is_active,
            "is_staff": obj.is_staff,
        }
