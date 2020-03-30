from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from members.models import UserImage, UserSpecific

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
        )


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = (
            'pk',
            'img_profile',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    # images = UserImageSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
            # 'images',
        )
