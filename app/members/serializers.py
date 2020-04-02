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

    # 회원가입 시 저장 정보
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


# 유저 정보
class UserSerializer(serializers.ModelSerializer):
    # images = UserImageSerializer(many=True)
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
        )


class UserImageSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = UserImage
        fields = (
            # 'user',
            'pk',
            'img_profile',
        )


# 카카오톡 계정 유저 정보
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


class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectTag
        fields = (
            'pk',
            'date_style',
            'relationship_style',
            'life_style',
            'charm',
        )


class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectStory
        fields = (
            'pk',
            'story',
            'content'
        )


class UserProfileSerializer(serializers.ModelSerializer):
    user_story = UserStorySerializer(source='user')

    class Meta:
        model = UserProfile
        fields = (
            'pk',
            # 'images',
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
            'user_story',
            # 'introduce',
        )

    def validate_user_story(self, value):
        return
