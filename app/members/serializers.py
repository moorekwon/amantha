from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import UserImage

User = get_user_model()


# 유저리스트
class UserSerializer(serializers.ModelSerializer):
    # images = UserImageSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
        )


#
# class UserProfileSerialzier(serializers.ModelSerializer):
#     class Meta:
#         model = UserSpecific
#         fields = (
#             'pk',
#             'nickname',
#             'job',
#         )


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = (
            'pk',
            'img_profile',
        )
