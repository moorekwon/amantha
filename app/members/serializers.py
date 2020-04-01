from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import UserImage, UserProfile, SendStar, SelectStory, SelectTag

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
            'password',
        )

    def save(self, **kwargs):
        email = self.validated_data['email']
        gender = self.validated_data['gender']
        password = self.validated_data['password']
        user = User.objects.create_user(
            email=email,
            gender=gender,
            password=password,
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    # images = UserImageSerializer(many=True)
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
        )


class KakaoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
        )


# class UserStarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SendStar
#         fields = (
#             'pk',
#             'star',
#         )
#
# class UserImageSerializer(serializers.ModelSerializer):
#     image = serializers.ImageField(use_url=True)
#
#     class Meta:
#         model = UserImage
#         fields = (
#             'pk',
#             'img_profile',
#         )


# class UserStorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SelectStory
#         fields = (
#             'pk',
#             'story',
#             'content'
#         )


# class UserTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SelectTag
#         fields = (
#             'pk',
#             'date_style',
#             'relationship_style',
#             'life_style',
#             'charm',
#         )


class UserProfileSerializer(serializers.ModelSerializer):
    # profile_image = UserImageSerializer(many=True)

    # story = UserStorySerializer(many=True)
    # tag = UserTagSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = (
            'pk',
            # 'profile_image',
            'nickname',
            'school',
            'major',
            'job',
            'company',
            'region',
            'birth',
            'tall',
            'body_shape',
            'personality',
            'blood_type',
            'smoking',
            'drinking',
            'introduce',
            # 'story',
            # 'tag',
        )
