# Generated by Django 2.2.11 on 2020-03-28 10:48

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('여자', '여자'), ('남자', '남자')], max_length=10)),
                ('job', models.CharField(blank=True, max_length=50)),
                ('school', models.CharField(blank=True, max_length=50)),
                ('age', models.CharField(blank=True, choices=[('20', 20), ('21', 21), ('22', 22), ('23', 23), ('24', 24), ('25', 25), ('26', 26), ('27', 27), ('28', 28), ('29', 29), ('30', 30), ('31', 31), ('32', 32), ('33', 33), ('34', 34), ('35', 35), ('36', 36), ('37', 37), ('38', 38), ('39', 39), ('40', 40), ('41', 41), ('42', 42), ('43', 43), ('44', 44), ('45', 45), ('46', 46), ('47', 47), ('48', 48), ('49', 49)], max_length=10)),
                ('region', models.CharField(blank=True, choices=[('서울', '서울'), ('경기', '경기'), ('인천', '인천'), ('대전', '대전'), ('충북', '충북'), ('충남', '충남'), ('강원', '강원'), ('부산', '부산'), ('경북', '경북'), ('경남', '경남'), ('대구', '대구'), ('울산', '울산'), ('광주', '광주'), ('전북', '전북'), ('전남', '전남'), ('제주', '제주')], max_length=30)),
                ('body_shape', models.CharField(blank=True, choices=[('보통체형', '보통체형'), ('통통한', '통통한'), ('살짝볼륨', '살짝볼륨'), ('글래머', '글래머'), ('마른', '마른'), ('슬림탄탄', '슬림탄탄')], max_length=50)),
                ('introduce', models.CharField(blank=True, max_length=150)),
                ('major', models.CharField(blank=True, max_length=50)),
                ('tall', models.CharField(blank=True, choices=[('140', 140), ('141', 141), ('142', 142), ('143', 143), ('144', 144), ('145', 145), ('146', 146), ('147', 147), ('148', 148), ('149', 149), ('150', 150), ('151', 151), ('152', 152), ('153', 153), ('154', 154), ('155', 155), ('156', 156), ('157', 157), ('158', 158), ('159', 159), ('160', 160), ('161', 161), ('162', 162), ('163', 163), ('164', 164), ('165', 165), ('166', 166), ('167', 167), ('168', 168), ('169', 169), ('170', 170), ('171', 171), ('172', 172), ('173', 173), ('174', 174), ('175', 175), ('176', 176), ('177', 177), ('178', 178), ('179', 179), ('180', 180), ('181', 181), ('182', 182), ('183', 183), ('184', 184), ('185', 185), ('186', 186), ('187', 187), ('188', 188), ('189', 189), ('190', 190), ('191', 191), ('192', 192), ('193', 193), ('194', 194), ('195', 195), ('196', 196), ('197', 197), ('198', 198), ('199', 199)], max_length=10)),
                ('personality', models.CharField(blank=True, choices=[('지적인', '지적인'), ('차분한', '차분한'), ('유머있는', '유머있는'), ('낙천적인', '낙천적인'), ('내향적인', '내향적인'), ('외향적인', '외향적인'), ('감성적인', '감성적인'), ('상냥한', '상냥한'), ('귀여운', '귀여운'), ('섹시한', '섹시한'), ('4차원인', '4차원인'), ('발랄한', '발랄한'), ('도도한', '도도한')], max_length=50)),
                ('blood_type', models.CharField(blank=True, choices=[('AB형', 'AB형'), ('A형', 'A형'), ('B형', 'B형'), ('O형', 'O형')], max_length=30)),
                ('drinking', models.CharField(blank=True, choices=[('가끔 마심', '가끔 마심'), ('어느정도 즐기는편', '어느정도 즐기는편'), ('술자리를 즐김', '술자리를 즐김'), ('마시지 않음', '마시지 않음')], max_length=60)),
                ('smoking', models.CharField(blank=True, choices=[('흡연', '흡연'), ('비흡연', '비흡연')], max_length=60)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserRibbon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ribbon', models.PositiveIntegerField(default=10)),
                ('when', models.DateTimeField(auto_now=True)),
                ('where', models.CharField(choices=[('관리자 기본 지급', '관리자 기본 지급'), ('회원심사 리본 지급', '회원심사 리본 지급'), ('상위 10% 이성(무료)', '상위 10% 이성(무료)'), ('테마 소개 프로필 확인', '테마 소개 프로필 확인'), ('아만다 픽 프로필 확인', '아만다 픽 프로필 확인')], max_length=60)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_profile', models.ImageField(upload_to='profile_images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SendStar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], max_length=30)),
                ('created', models.DateTimeField(auto_now=True)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_sendstar_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sendstar_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SendLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_sendlike_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sendlike_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SelectTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_style', models.CharField(blank=True, choices=[('인스타감성 카페가기', '인스타감성 카페가기'), ('퇴근 후 치맥하기', '퇴근 후 치맥하기')], max_length=60)),
                ('relationship_style', models.CharField(blank=True, choices=[('연상이 좋아요', '연상이 좋아요'), ('연상보다 연하', '연상보다 연하')], max_length=60)),
                ('life_style', models.CharField(blank=True, choices=[('패션에 관심 많아요', '패션에 관심 많아요'), ('여행 자주 가요', '여행 자주 가요')], max_length=60)),
                ('charm', models.CharField(blank=True, choices=[('고기를 잘 구워요', '고기를 잘 구워요'), ('커리어 중요해요', '커리어 중요해요')], max_length=60)),
                ('created', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SelectStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story', models.CharField(choices=[('이상적인 첫 소개팅 장소', '이상적인 첫 소개팅 장소'), ('내 외모중 가장 마음에 드는 곳은', '내 외모중 가장 마음에 드는 곳은'), ('남들보다 이것 하나는 자신있어요', '남들보다 이것 하나는 자신있어요')], max_length=60)),
                ('content', models.CharField(max_length=60)),
                ('created', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='like_users',
            field=models.ManyToManyField(related_name='send_me_like_users', through='members.SendLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='star_users',
            field=models.ManyToManyField(related_name='send_me_star_users', through='members.SendStar', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]