from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import UserImage

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'username',
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
            'username',
            # 'images',
        )
