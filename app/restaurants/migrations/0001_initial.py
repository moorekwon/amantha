
# Generated by Django 2.2.12 on 2020-04-09 12:21

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='식당이름')),
                ('address1', models.CharField(blank=True, default='없음', max_length=100, verbose_name='식당주소')),
                ('name_address1_unique', models.CharField(max_length=100, unique=True, verbose_name='primary_key')),
                ('address2', models.CharField(blank=True, default='없음', max_length=100, verbose_name='식당지번주소')),
                ('point', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, verbose_name='식당평점')),
                ('phone', phone_field.models.PhoneField(blank=True, default='없음', help_text='Contact phone number', max_length=31, null=True)),
                ('price_range', models.CharField(blank=True, default='없음', max_length=100, null=True, verbose_name='식당가격대')),
                ('parking', models.CharField(blank=True, default='없음', max_length=200, null=True, verbose_name='주차여부')),
                ('opening_hours', models.CharField(blank=True, default='없음', max_length=100, null=True, verbose_name='오픈시간')),
                ('menu', models.CharField(blank=True, default='없음', max_length=300, null=True, verbose_name='식당메뉴')),
                ('restaurant_type', models.CharField(blank=True, default='없음', max_length=100, null=True, verbose_name='음식점종류')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='수정날짜')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=30, verbose_name='카테고리_식당_섬네일')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='수정날짜')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurants.Restaurant', verbose_name='지역_식당')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='restaurant/images')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='수정날짜')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurants.Restaurant', verbose_name='이미지_식당')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=10, verbose_name='카테고리_유형')),
                ('thumbnail', models.ImageField(blank=True, upload_to='category/images', verbose_name='카테고리_식당_섬네일')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='수정날짜')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurants.Restaurant', verbose_name='카테고리_식당')),
            ],
        ),
    ]
