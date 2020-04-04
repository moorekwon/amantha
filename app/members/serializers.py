from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import UserImage, SelectStory, UserInfo, UserRibbon, SelectTag

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


# 유저의 계정 정보 (전체 유저 조회용)
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
        )


# 카카오톡 계정 유저 정보
class KakaoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
        )


# UserImage 필드정보
class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = (
            'pk',
            'user_image',
        )


# UserInfo 필드정보
class UserInfoSerializer(serializers.ModelSerializer):
    age = UserInfo.age
    average_star = UserInfo.average_star

    class Meta:
        model = UserInfo
        fields = (
            'pk',
            'average_star',
            'nickname',
            'school',
            'major',
            'job',
            'company',
            'region',
            'birth',
            'age',
            'tall',
            'body_shape',
            'personality',
            'blood_type',
            'smoking',
            'drinking',
            'introduce',
        )


# SelectStory 필드정보
class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectStory
        fields = (
            'pk',
            'story',
            'content'
        )


# SelectTag 필드정보
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


# UserRibbon 필드정보
class UserRibbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRibbon
        fields = (
            'pk',
            'ribbon',
            'when',
            'where',
        )


# 유저의 전체프로필 정보 (조회용)
class UserProfileSerializer(serializers.ModelSerializer):
    user_ribbon = UserRibbonSerializer(source='userribbon.ribbon')
    user_image = UserImageSerializer(many=True, source='userimage_set')
    user_info = UserInfoSerializer(source='userinfo')
    user_story = UserStorySerializer(many=True, source='selectstory_set')
    user_tag = UserTagSerializer(many=True, source='selecttag_set')

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
            'user_image',
            'user_info',
            'user_story',
            'user_tag',
            'user_ribbon',
        )
