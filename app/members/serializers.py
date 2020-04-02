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


class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectStory
        fields = (
            'pk',
            'story',
            'content'
        )


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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'pk',
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


# 유저 정보
class UserSerializer(serializers.ModelSerializer):
    user_image = UserImageSerializer(many=True, source='userimage_set')
    user_profile = UserProfileSerializer(source='userprofile')
    user_story = UserStorySerializer(many=True, source='selectstory_set')
    user_tag = UserTagSerializer(many=True, source='selecttag_set')

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
            'user_image',
            'user_profile',
            'user_story',
            'user_tag',
        )
