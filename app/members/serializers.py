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
            'image',
        )


# UserInfo 필드정보
class UserInfoSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source='user.age', read_only=True)
    averageStar = serializers.IntegerField(source='user.average_star', read_only=True)
    bodyShape = serializers.CharField(source='body_shape', required=False)
    bloodType = serializers.CharField(source='blood_type', required=False)

    class Meta:
        model = UserInfo
        fields = (
            'pk',
            'averageStar',
            'nickname',
            'school',
            'major',
            'job',
            'company',
            'region',
            'birth',
            'age',
            'tall',
            'bodyShape',
            'personality',
            'bloodType',
            'smoking',
            'drinking',
            'religion',
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
    paidRibbon = serializers.IntegerField(source='paid_ribbon')
    currentRibbon = serializers.IntegerField(source='current_ribbon', read_only=True)

    class Meta:
        model = UserRibbon
        fields = (
            'pk',
            'paidRibbon',
            'currentRibbon',
            'when',
            'where',
        )


# 유저의 전체프로필 정보 (조회용)
class UserProfileSerializer(serializers.ModelSerializer):
    sendMeLikeUsers = serializers.ListField(
        child=serializers.CharField(), source='send_me_like_users.all'
    )
    images = UserImageSerializer(many=True, source='userimage_set')
    info = UserInfoSerializer(source='userinfo')
    stories = UserStorySerializer(many=True, source='selectstory_set')
    tags = UserTagSerializer(many=True, source='selecttag_set')
    currentRibbon = serializers.CharField(source='userribbon_set.last.current_ribbon')

    class Meta:
        model = User
        fields = (
            'email',
            'gender',
            'currentRibbon',
            'sendMeLikeUsers',
            'images',
            'info',
            'stories',
            'tags',
        )
