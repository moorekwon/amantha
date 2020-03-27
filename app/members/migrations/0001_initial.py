# Generated by Django 2.2.11 on 2020-03-27 17:13

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
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
                ('age', models.CharField(choices=[('20', 20), ('21', 21), ('22', 22), ('23', 23), ('24', 24), ('25', 25), ('26', 26), ('27', 27), ('28', 28), ('29', 29), ('30', 30), ('31', 31), ('32', 32), ('33', 33), ('34', 34), ('35', 35), ('36', 36), ('37', 37), ('38', 38), ('39', 39), ('40', 40), ('41', 41), ('42', 42), ('43', 43), ('44', 44), ('45', 45), ('46', 46), ('47', 47), ('48', 48), ('49', 49)], max_length=10)),
                ('job', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=30)),
                ('school', models.CharField(max_length=50)),
                ('tall', models.CharField(choices=[('140', 140), ('141', 141), ('142', 142), ('143', 143), ('144', 144), ('145', 145), ('146', 146), ('147', 147), ('148', 148), ('149', 149), ('150', 150), ('151', 151), ('152', 152), ('153', 153), ('154', 154), ('155', 155), ('156', 156), ('157', 157), ('158', 158), ('159', 159), ('160', 160), ('161', 161), ('162', 162), ('163', 163), ('164', 164), ('165', 165), ('166', 166), ('167', 167), ('168', 168), ('169', 169), ('170', 170), ('171', 171), ('172', 172), ('173', 173), ('174', 174), ('175', 175), ('176', 176), ('177', 177), ('178', 178), ('179', 179), ('180', 180), ('181', 181), ('182', 182), ('183', 183), ('184', 184), ('185', 185), ('186', 186), ('187', 187), ('188', 188), ('189', 189), ('190', 190), ('191', 191), ('192', 192), ('193', 193), ('194', 194), ('195', 195), ('196', 196), ('197', 197), ('198', 198), ('199', 199)], max_length=10)),
                ('body_shape', models.CharField(blank=True, choices=[('보통체형', '보통체형'), ('통통한', '통통한'), ('살짝볼륨', '살짝볼륨'), ('글래머', '글래머'), ('마른', '마른'), ('슬림탄탄', '슬림탄탄')], max_length=50)),
                ('personality', models.CharField(blank=True, choices=[('지적인', '지적인'), ('차분한', '차분한'), ('유머있는', '유머있는'), ('낙천적인', '낙천적인'), ('내향적인', '내향적인'), ('외향적인', '외향적인'), ('감성적인', '감성적인'), ('상냥한', '상냥한'), ('귀여운', '귀여운'), ('섹시한', '섹시한'), ('4차원인', '4차원인'), ('발랄한', '발랄한'), ('도도한', '도도한')], max_length=50)),
                ('tags', models.CharField(blank=True, choices=[('date_style', (('인스타감성 카페가기', '인스타감성 카페가기'), ('퇴근 후 치맥하기', '퇴근 후 치맥하기'))), ('life_style', (('패션에 관심 많아요', '패션에 관심 많아요'), ('여행 자주 가요', '여행 자주 가요'))), ('charm', (('고기를 잘 구워요', '고기를 잘 구워요'), ('커리어 중요해요', '커리어 중요해요'))), ('relationship_style', (('연상이 좋아요', '연상이 좋아요'), ('연상보다 연하', '연상보다 연하')))], max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
    ]
