from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import UserImage, SelectStory, UserInfo, UserRibbon, Tag

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
            # 'where',
        )


# class TagTypeSerializer(serializers.ModelSerializer):
#     tags = UserTagSerializer(many=True, read_only=True)
#
#     dateStyle = serializers.CharField(source='date_style_tag.all')
#
#     class Meta:
#         model = User
#         fields = (
#             'tags',
#             'dateStyle',
#         )


class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
        )


class TagTypeSerializer(serializers.ModelSerializer):
    dateStyle = UserTagSerializer(source='date_style_tag', many=True, required=False)
    lifeStyle = UserTagSerializer(source='life_style_tag', many=True, required=False)
    charm = UserTagSerializer(source='charm_tag', many=True, required=False)
    relationshipStyle = UserTagSerializer(source='relationship_style_tag', many=True, required=False)

    class Meta:
        model = User
        fields = (
            'dateStyle',
            'lifeStyle',
            'charm',
            'relationshipStyle',
        )


# 유저의 전체프로필 정보 (조회용)
class UserProfileSerializer(serializers.ModelSerializer):
    currentRibbon = serializers.IntegerField(source='userribbon_set.last.current_ribbon')
    profilePercentage = serializers.FloatField(source='userinfo.profile_percentage')
    sendMeLikeUsers = serializers.ListField(
        child=serializers.EmailField(), source='send_me_like_users.all'
    )
    images = UserImageSerializer(many=True, source='userimage_set')
    info = UserInfoSerializer(source='userinfo')
    stories = UserStorySerializer(many=True, source='selectstory_set')

    # 표시 방법 재검토 필요
    dateStyleTag = UserTagSerializer(source='date_style_tag', many=True)
    lifeStyleTag = UserTagSerializer(source='life_style_tag', many=True)
    charmTag = UserTagSerializer(source='charm_tag', many=True)
    relationshipStyleTag = UserTagSerializer(source='relationship_style_tag', many=True)

    class Meta:
        model = User
        fields = (
            'email',
            'gender',
            'currentRibbon',
            'profilePercentage',
            'sendMeLikeUsers',
            'images',
            'info',
            'stories',

            'dateStyleTag',
            'lifeStyleTag',
            'charmTag',
            'relationshipStyleTag',
        )
