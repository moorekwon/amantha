from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# 유저 프로필
class User(AbstractUser):
    GENDER = (
        ('여자', '여자'),
        ('남자', '남자'),
    )

    BODY_SHAPE = (
        ('보통체형', '보통체형'),
        ('통통한', '통통한'),
        ('살짝볼륨', '살짝볼륨'),
        ('글래머', '글래머'),
        ('마른', '마른'),
        ('슬림탄탄', '슬림탄탄'),
    )

    # 여러 개 선택 가능하게 하도록 해야함
    PERSONALITY = (
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

    # 방식 수정 필요
    TAGS = (
        ('date_style', (
            ('인스타감성 카페가기', '인스타감성 카페가기'),
            ('퇴근 후 치맥하기', '퇴근 후 치맥하기'),
        )),
        ('life_style', (
            ('패션에 관심 많아요', '패션에 관심 많아요'),
            ('여행 자주 가요', '여행 자주 가요'),
        )),
        ('charm', (
            ('고기를 잘 구워요', '고기를 잘 구워요'),
            ('커리어 중요해요', '커리어 중요해요'),
        )),
        ('relationship_style', (
            ('연상이 좋아요', '연상이 좋아요'),
            ('연상보다 연하', '연상보다 연하'),
        ))
    )

    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER, max_length=10)
    age = models.CharField(choices=((str(x), x) for x in range(20, 50)), max_length=10)
    job = models.CharField(max_length=50)
    region = models.CharField(max_length=30)
    school = models.CharField(max_length=50)
    tall = models.CharField(choices=((str(x), x) for x in range(140, 200)), max_length=10)
    body_shape = models.CharField(choices=BODY_SHAPE, blank=True, max_length=50)
    personality = models.CharField(choices=PERSONALITY, blank=True, max_length=50)
    tags = models.CharField(choices=TAGS, blank=True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
