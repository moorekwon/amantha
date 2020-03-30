from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, nickname=None, password=None):
        if not email:
            raise ValueError('email 주소가 있어야 합니다.')

        user = self.model(email=self.normalize_email(email), nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(email=email, password=password, nickname=nickname)
        user.is_superuser = True
        user.save(using=self._db)
        return user


# 유저 프로필
class User(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('여자', '여자'),
        ('남자', '남자'),
    )

    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER, max_length=10)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender', ]

    def profile_percentage(self):
        pass


# 유저 생성 후 기입할 프로필 정보
class UserSpecific(models.Model):
    REGION = (
        ('서울', '서울'),
        ('경기', '경기'),
        ('인천', '인천'),
        ('대전', '대전'),
        ('충북', '충북'),
        ('충남', '충남'),
        ('강원', '강원'),
        ('부산', '부산'),
        ('경북', '경북'),
        ('경남', '경남'),
        ('대구', '대구'),
        ('울산', '울산'),
        ('광주', '광주'),
        ('전북', '전북'),
        ('전남', '전남'),
        ('제주', '제주'),
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
    BLOOD_TYPE = (
        ('AB형', 'AB형'),
        ('A형', 'A형'),
        ('B형', 'B형'),
        ('O형', 'O형'),
    )
    DRINKING = (
        ('가끔 마심', '가끔 마심'),
        ('어느정도 즐기는편', '어느정도 즐기는편'),
        ('술자리를 즐김', '술자리를 즐김'),
        ('마시지 않음', '마시지 않음'),
    )
    SMOKING = (
        ('흡연', '흡연'),
        ('비흡연', '비흡연'),
    )

    nickname = models.CharField(unique=True, max_length=60)
    job = models.CharField(max_length=50, blank=True)
    school = models.CharField(max_length=50, blank=True)
    age = models.CharField(choices=((str(x), x) for x in range(20, 50)), max_length=10, blank=True)
    region = models.CharField(choices=REGION, max_length=30, blank=True)
    body_shape = models.CharField(choices=BODY_SHAPE, blank=True, max_length=50)
    introduce = models.CharField(max_length=150, blank=True)
    major = models.CharField(max_length=50, blank=True)
    tall = models.CharField(choices=((str(x), x) for x in range(140, 200)), max_length=10, blank=True)
    personality = models.CharField(choices=PERSONALITY, blank=True, max_length=50)
    blood_type = models.CharField(choices=BLOOD_TYPE, max_length=30, blank=True)
    drinking = models.CharField(choices=DRINKING, max_length=60, blank=True)
    smoking = models.CharField(choices=SMOKING, max_length=60, blank=True)
    star_users = models.ManyToManyField('self', through='SendStar', related_name='send_me_star_users',
                                        symmetrical=False)
    like_users = models.ManyToManyField('self', through='SendLike', related_name='send_me_like_users',
                                        symmetrical=False)


# many-to-one 관계
# 한 번에 여러 개 post 가능하도록 해야 함
class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img_profile = models.ImageField(upload_to='profile_images/')


# 스토리 등록
class SelectStory(models.Model):
    STORY = (
        ('이상적인 첫 소개팅 장소', '이상적인 첫 소개팅 장소'),
        ('내 외모중 가장 마음에 드는 곳은', '내 외모중 가장 마음에 드는 곳은'),
        ('남들보다 이것 하나는 자신있어요', '남들보다 이것 하나는 자신있어요'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.CharField(choices=STORY, max_length=60)
    content = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now=True)


# 태그 등록
class SelectTag(models.Model):
    DATE_STYLE = (
        ('인스타감성 카페가기', '인스타감성 카페가기'),
        ('퇴근 후 치맥하기', '퇴근 후 치맥하기'),
    )
    RELATIONSHIP_STYLE = (
        ('연상이 좋아요', '연상이 좋아요'),
        ('연상보다 연하', '연상보다 연하'),
    )
    LIFE_STYLE = (
        ('패션에 관심 많아요', '패션에 관심 많아요'),
        ('여행 자주 가요', '여행 자주 가요'),
    )
    CHARM = (
        ('고기를 잘 구워요', '고기를 잘 구워요'),
        ('커리어 중요해요', '커리어 중요해요'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_style = models.CharField(choices=DATE_STYLE, blank=True, max_length=60)
    relationship_style = models.CharField(choices=RELATIONSHIP_STYLE, blank=True, max_length=60)
    life_style = models.CharField(choices=LIFE_STYLE, blank=True, max_length=60)
    charm = models.CharField(choices=CHARM, blank=True, max_length=60)
    created = models.DateTimeField(auto_now=True)


# one-to-one 관계
# 리본 사용
# 첫 유저 생성 시 바로 생성되어야 함 (default 값으로)
class UserRibbon(models.Model):
    WHERE = (
        ('관리자 기본 지급', '관리자 기본 지급'),
        ('회원심사 리본 지급', '회원심사 리본 지급'),
        ('상위 10% 이성(무료)', '상위 10% 이성(무료)'),
        ('테마 소개 프로필 확인', '테마 소개 프로필 확인'),
        ('아만다 픽 프로필 확인', '아만다 픽 프로필 확인'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ribbon = models.PositiveIntegerField(default=10)
    when = models.DateTimeField(auto_now=True)
    where = models.CharField(choices=WHERE, max_length=60, default='관리자 기본 지급')

    def add_subtract(self):
        pass

    def accumulate(self):
        pass


# 리본 결제
# class PayRibbon(models.Model):
#     pass


# 별점 주기
class SendStar(models.Model):
    user = models.ForeignKey(User, related_name='user_sendstar_set', on_delete=models.CASCADE)
    partner = models.ForeignKey(User, related_name='partner_sendstar_set', on_delete=models.CASCADE)
    star = models.CharField(choices=((str(x), x) for x in range(1, 6)), max_length=30)
    created = models.DateTimeField(auto_now=True)


# 좋아요 주기
class SendLike(models.Model):
    user = models.ForeignKey(User, related_name='user_sendlike_set', on_delete=models.CASCADE)
    partner = models.ForeignKey(User, related_name='partner_sendlike_set', on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
