from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import UserImage, UserInfo, UserRibbon, Tag, UserIdealType, Pick, Star, Story

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
            'status',
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
    user = serializers.ReadOnlyField(source='userimage_set')

    class Meta:
        model = UserImage
        fields = (
            'user',
            'pk',
            'image',
        )


# UserInfo 필드정보
class UserInfoSerializer(serializers.ModelSerializer):
    PERSONALITIES = (
        ('지적인', '지적인'),
        ('차분한', '차분한'),
        ('유머있는', '유머있는'),
        ('낙천적인', '낙천적인'),
        ('내향적인', '내향적인'),
        ('외향적인', '외향적인'),
        ('감성적인', '감성적인'),
        ('상냥한', '상냥한'),
        ('귀여운', '귀여운'),
        ('섹시한', '섹시한'),
        ('4차원인', '4차원인'),
        ('발랄한', '발랄한'),
        ('도도한', '도도한'),
    )

    age = serializers.IntegerField(source='user.age', read_only=True)
    bodyShape = serializers.CharField(source='body_shape', required=False)
    # personality 모델 필드와 차이가 없는데 구지 serializer에서 한번 더 써줘야 할지 의문
    personalities = serializers.MultipleChoiceField(choices=PERSONALITIES, source='personality', required=False)
    bloodType = serializers.CharField(source='blood_type', required=False)

    class Meta:
        model = UserInfo
        fields = (
            'nickname',
            'birth',
            'age',
            'school',
            'major',
            'job',
            'company',
            'region',
            'tall',
            'bodyShape',
            'personalities',
            'bloodType',
            'smoking',
            'drinking',
            'religion',
            'introduce',
        )


# Story 필드정보
class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
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
        )


class UserPickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pick
        fields = (
            'user',
            'partner',
            'created',
        )


class UserStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = (
            'user',
            'partner',
            'star',
            'created',
        )


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


class IdealTypeSerializer(serializers.ModelSerializer):
    PERSONALITIES = (
        ('지적인', '지적인'),
        ('차분한', '차분한'),
        ('유머있는', '유머있는'),
        ('낙천적인', '낙천적인'),
        ('내향적인', '내향적인'),
        ('외향적인', '외향적인'),
        ('감성적인', '감성적인'),
        ('상냥한', '상냥한'),
        ('귀여운', '귀여운'),
        ('섹시한', '섹시한'),
        ('4차원인', '4차원인'),
        ('발랄한', '발랄한'),
        ('도도한', '도도한'),
    )

    ageFrom = serializers.IntegerField(source='age_from', required=True)
    ageTo = serializers.IntegerField(source='age_to', required=True)
    tallFrom = serializers.IntegerField(source='tall_from', required=False)
    tallTo = serializers.IntegerField(source='tall_to', required=False)
    personalities = serializers.MultipleChoiceField(choices=PERSONALITIES, source='personality', required=False)
    bodyShape = serializers.CharField(source='body_shape', required=False)

    class Meta:
        model = UserIdealType
        fields = (
            'ageFrom',
            'ageTo',
            'region',
            'region2',
            'tallFrom',
            'tallTo',
            'bodyShape',
            'personalities',
            'religion',
            'smoking',
            'drinking',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    averageStar = serializers.FloatField(source='average_star')
    currentRibbon = serializers.IntegerField(source='userribbon_set.last.current_ribbon')
    profilePercentage = serializers.FloatField(source='userinfo.profile_percentage')
    images = UserImageSerializer(many=True, source='userimage_set')
    info = UserInfoSerializer(source='userinfo')
    stories = UserStorySerializer(many=True, source='story_set')
    tags = TagTypeSerializer(source='tag')
    idealTypeInfo = IdealTypeSerializer(source='useridealtype_set', many=True)
    ribbonHistory = UserRibbonSerializer(source='userribbon_set', many=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'gender',
            'status',
            'averageStar',
            'currentRibbon',
            'profilePercentage',
            'images',
            'info',
            'stories',
            'tags',
            'idealTypeInfo',
            'ribbonHistory',
        )
