import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from rest_framework.fields import MultipleChoiceField


class UserManager(BaseUserManager):
    def create_user(self, email, gender=None, password=None):
        if not email:
            raise ValueError('email 주소가 있어야 합니다.')

        user = self.model(email=self.normalize_email(email), gender=gender)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, gender, password):
        user = self.create_user(email=email, password=password, gender=gender)
        user.is_staff = True
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

    is_staff = True

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender', ]

    star_users = models.ManyToManyField('self', through='SendStar', related_name='send_me_star_users',
                                        symmetrical=False)
    like_users = models.ManyToManyField('self', through='SendLike', related_name='send_me_like_users',
                                        symmetrical=False)

    # 유저의 현재 평균 별점
    def average_star(self):
        partners = self.partner_sendstar_set.all()
        print('partners >> ', partners)
        star = [int(partner.star) for partner in partners]
        if len(star) > 0:
            print('sum(star) / len(star) >> ', sum(star) / len(star))
            return format(sum(star) / len(star), '.2f')
        else:
            print(0)
            return 0

    # 유저의 현재 나이
    def age(self):
        today = datetime.date.today()
        today_year = str(today).split('-')[0]
        if self.userinfo.birth:
            birth_year = str(self.userinfo.birth).split('-')[0]
            return int(today_year) - int(birth_year) + 1
        return None


# 유저 생성 후 기입할 프로필 정보
class UserInfo(models.Model):
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
    RELIGION = (
        ('종교 없음', '종교 없음'),
        ('기독교', '기독교'),
        ('천주교', '천주교'),
        ('불교', '불교'),
        ('원불교', '원불교'),
        ('유교', '유교'),
        ('이슬람교', '이슬람교'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(unique=True, max_length=60)
    job = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=60, blank=True)
    school = models.CharField(max_length=50, blank=True)
    birth = models.DateField(blank=False)
    region = models.CharField(choices=REGION, max_length=30, blank=True)
    body_shape = models.CharField(choices=BODY_SHAPE, blank=True, max_length=50)
    major = models.CharField(max_length=50, blank=True)
    tall = models.CharField(choices=((str(x), x) for x in range(140, 200)), max_length=10, blank=True)
    personality = models.CharField(choices=PERSONALITY, blank=True, max_length=100)
    blood_type = models.CharField(choices=BLOOD_TYPE, max_length=30, blank=True)
    drinking = models.CharField(choices=DRINKING, max_length=60, blank=True)
    smoking = models.CharField(choices=SMOKING, max_length=60, blank=True)
    religion = models.CharField(choices=RELIGION, max_length=60, blank=True)
    introduce = models.CharField(max_length=150, blank=True)

    # 유저의 현재 프로필 완성도
    def profile_percentage(self):
        story = self.user.selectstory_set.all()
        date_style = self.user.selecttag_set.all()
        life_style = self.user.selecttag_set.all()
        charm = self.user.selecttag_set.all()
        relationship_style = self.user.selecttag_set.all()

        info_list = [self.job, self.company, self.school, self.region, self.body_shape, self.major, self.tall,
                     self.personality, self.blood_type, self.drinking, self.smoking, self.religion, self.introduce,
                     story, date_style, life_style, charm, relationship_style]

        return_list = []
        for infos in info_list:
            if not infos:
                return_list.append(0)
            else:
                return_list.append(1)

        if sum(return_list) == 0:
            profile_percentage = 0
        else:
            profile_percentage = format(sum(return_list) / len(return_list) * 100, '.1f')
        return profile_percentage


# 별점 주기
class SendStar(models.Model):
    user = models.ForeignKey(User, related_name='user_sendstar_set', on_delete=models.CASCADE)
    partner = models.ForeignKey(User, related_name='partner_sendstar_set', on_delete=models.CASCADE)
    star = models.CharField(choices=((str(x), x) for x in range(1, 6)), max_length=30)
    created = models.DateTimeField(auto_now=True)


# many-to-one 관계
# 한 번에 여러 개 post 가능하도록 해야 함
class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/')


# 스토리 등록
class SelectStory(models.Model):
    STORY = (
        (1, '이상적인 첫 소개팅 장소'),
        (2, '내 외모중 가장 마음에 드는 곳은'),
        (3, '남들보다 이것 하나는 자신있어요'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.CharField(choices=STORY, max_length=60, blank=True)
    content = models.CharField(max_length=60, blank=True)
    created = models.DateTimeField(auto_now=True)


# 태그 등록
class SelectTag(models.Model):
    DATE_STYLE = (
        (1, '인스타감성 카페가기'),
        (2, '퇴근 후 치맥하기'),
    )
    RELATIONSHIP_STYLE = (
        (1, '연상이 좋아요'),
        (2, '연상보다 연하'),
    )
    LIFE_STYLE = (
        (1, '패션에 관심 많아요'),
        (2, '여행 자주 가요'),
    )
    CHARM = (
        (1, '고기를 잘 구워요'),
        (2, '커리어 중요해요'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_style = MultipleChoiceField(choices=DATE_STYLE, allow_blank=True)
    relationship_style = MultipleChoiceField(choices=RELATIONSHIP_STYLE, allow_blank=True)
    life_style = MultipleChoiceField(choices=LIFE_STYLE, allow_blank=True)
    charm = MultipleChoiceField(choices=CHARM, allow_blank=True)
    created = models.DateTimeField(auto_now=True)


# one-to-one 관계
# 리본 사용
# 첫 유저 생성 시 바로 생성되어야 함 (default 값으로)
class UserRibbon(models.Model):
    # WHERE = (
    #     (1, '관리자 기본 지급'),
    #     (2, '아만다 픽 프로필 확인'),
    #     (3, '회원심사 리본 지급'),
    #     (4, '상위 10% 이성(무료)'),
    #     (5, '테마 소개 프로필 확인'),
    # )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # paid_ribbon과 where를 연결시켜줘야 하는데...
    paid_ribbon = models.IntegerField()
    current_ribbon = models.PositiveIntegerField()
    when = models.DateTimeField(auto_now=True)

    # where = models.CharField(choices=WHERE, max_length=60, default=1)

    # 첫 관리자 기본 지급 제외, 리본 지급 추가때마다 이전 current_ribbon에서 현재 paid_ribbon을 빼 현재 current_ribbon에 저장
    def save(self, *args, **kwargs):
        # where의 각 인덱스별 paid_ribbon 지정
        # pay = [10, -3, -5, -5, -7]
        # rib = pay[int(self.where) - 1]
        # self.paid_ribbon = rib

        ribbons = UserRibbon.objects.filter(user=self.user)

        if len(ribbons) == 0:
            pass
        else:
            pre = ribbons[len(ribbons) - 1]

            self.current_ribbon = pre.current_ribbon + self.paid_ribbon
        super().save(*args, **kwargs)


# 리본 결제
# class PayRibbon(models.Model):
#     pass


# 좋아요 주기
class SendLike(models.Model):
    user = models.ForeignKey(User, related_name='user_sendlike_set', on_delete=models.CASCADE)
    partner = models.ForeignKey(User, related_name='partner_sendlike_set', on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
