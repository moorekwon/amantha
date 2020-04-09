#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from django.db import OperationalError, IntegrityError
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev_dooh')
django.setup()

from restaurants.models import Restaurant, RestaurantCategory, RestaurantImages, RestaurantLocation


def firstpage_web_crawler():
    chrom_path = '../chromedriver'
    rootPath = 'https://www.mangoplate.com/'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    driver = webdriver.Chrome(chrom_path, chrome_options=options)

    driver.get(rootPath)
    html = driver.page_source
    r = open('../home_first_page.txt', mode='w', encoding='utf-8')
    r.write(html)
    print(rootPath)
    r.close()

    driver.quit()


firstpage_web_crawler()

html = open('../home_first_page.txt', "r").read()
song_soup = BeautifulSoup(html)
soup = BeautifulSoup(html, 'html.parser')

home_div_top_list_slide = soup.select(
    'body > main > article > section:nth-child(3) > div.slider-container.toplist-slider > div > div > div')
big_category = soup.select_one('div.module_title_wrap').select_one('h2').get_text(strip=True).replace(" ", "")
home_trust_list = soup.select_one('div.slick-track')
one_ul_two_a = home_trust_list.select('ul')
category_data = {

}
for text in one_ul_two_a:
    select_list = text.select('a')
    select_img = text.select('img')
    for data, img in zip(select_list, select_img):
        category_data[data.select('span.title')[0].get_text(strip=True)] = {
            "href": data['href'],
            "title": data.select('span.title')[0].get_text(strip=True),
            "sub_title": data.select('p')[0].get_text(strip=True),
            "img_uri": img['src'],
            "big_category": big_category,
        }

print(category_data)

import os

path = '../data/' + big_category + '/'
file_list = [i for i in os.listdir(path) if '곳' in i]
print(file_list)

detail_page_craw = {}
path = '../data/' + big_category + '/'
for category_detail_list in file_list:
    file_name = os.listdir(path + category_detail_list + '/')
    parent_text = {}
    for restaurant in file_name:

        try:
            html = open(path + category_detail_list + '/' + restaurant, "r").read()
            health_restaurant_detail = BeautifulSoup(html)
            # text 크롤링
            div_inner = health_restaurant_detail.select_one('div.column-contents').select_one('div.inner')
            section_restaurant_detail = div_inner.select_one('section.restaurant-detail')
            div_restaurant_title_wrap = section_restaurant_detail.select_one('div.restaurant_title_wrap')
            span_title = div_restaurant_title_wrap.select_one('span.title')
            restaurant_title = span_title.select_one('h1').get_text(strip=True)
            restaurant_point = span_title.select_one('strong.rate-point').select_one('span').get_text(strip=True)
            tbody = section_restaurant_detail.select_one('table.info').select_one('tbody')
            # images 크롤링
            asid_restaurant = health_restaurant_detail.select_one('aside.restaurant-photos')
            div_owl_wrapper = asid_restaurant.select_one('div.owl-wrapper')
            div_owl_item = div_owl_wrapper.select('div.owl-item')
        except AttributeError as ex:
            print(f'page 없는 데이터 존재', ex)
        ###################################################################################
        image_contents = {

        }
        for index, data in enumerate(div_owl_item):
            image_contents['image_' + str(index)] = data.select_one('meta')['content']
        restaurant_detail_fields = {
            "title": restaurant_title,
            "images": image_contents,
        }
        #     print(restaurant_detail_fields)
        for i in tbody.select('tr'):

            restaurant_detail_fields[i.select_one('th').get_text(strip=True)] = i.select_one('td').get_text(strip=True)

            if not i.select_one('span.Restaurant__InfoAddress--Rectangle') == None:
                restaurant_detail_fields[i.select_one('span.Restaurant__InfoAddress--Rectangle').get_text(strip=True)] \
                    = i.select_one('span.Restaurant__InfoAddress--Text').get_text(strip=True)
        parent_text[restaurant.split(".")[0]] = restaurant_detail_fields

    detail_page_craw[category_detail_list] = parent_text

print(detail_page_craw)
print(Restaurant)


def restaurant_create():

    for catetory_name, restaurant_name in detail_page_craw.items():
        #     print( restaurant_factors)
        for key, restaurant_factors in restaurant_name.items():

            try:
                restaurant_factors['title']
                restaurant_factors['주소']
                restaurant_factors['지번']
                restaurant_factors['가격대']

            except KeyError:
                print(file_name, '   못만듬')
                print('\n')
                continue
            try:
                restaurant_factors['주차']
            except KeyError:
                restaurant_factors['주차'] = '정보없음'

            try:
                restaurant_factors['전화번호']
            except KeyError:
                restaurant_factors['전화번호'] = '010-0000-0000'
            try:
                restaurant_factors['음식 종류']
            except KeyError:
                restaurant_factors['음식 종류'] = '정보없음'

            unique = catetory_name + restaurant_factors['title'].replace(" ", "") + restaurant_factors['주소'].replace(
                " ",
                "")
            print(unique)
            name = restaurant_factors['title'].replace(" ", "")
            print(restaurant_factors['title'].replace(" ", ""))

            address1 = restaurant_factors['주소'].replace(" ", "")
            print(restaurant_factors['주소'].replace(" ", ""))

            address2 = restaurant_factors['지번'].replace(" ", "")
            print(restaurant_factors['지번'].replace(" ", ""))

            restaurant_type = restaurant_factors['음식 종류'].replace(" ", "")
            print(restaurant_factors['음식 종류'].replace(" ", ""))

            price_range = restaurant_factors['가격대'].replace(" ", "")
            print(restaurant_factors['가격대'].replace(" ", ""))

            phone = restaurant_factors['전화번호'].replace(" ", "")
            print(restaurant_factors['전화번호'].replace(" ", ""))

            parking = restaurant_factors['주차'].replace(" ", "")
            print(restaurant_factors['주차'].replace(" ", ""))

            try:

                Restaurant.objects.create(
                    name_address1_unique=unique,
                    name=name,
                    address1=address1,
                    address2=address2,
                    restaurant_type=restaurant_type,
                    price_range=price_range,
                    phone=phone,
                    parking=parking,
                )
            except OperationalError:
                print('unique 에러여서 넘어감')
                continue


def restaurant_category_create():
    for catetory_name, restaurant_name in detail_page_craw.items():
        for key, restaurant_factors in restaurant_name.items():

            print(restaurant_factors['images']['image_0'])
            unique = catetory_name + restaurant_factors['title'].replace(" ", "") + restaurant_factors['주소'].replace(
                " ",
                "")
            aa = Restaurant.objects.get(name_address1_unique=unique)
            print(aa.name)
            try:

                RestaurantCategory.objects.create(
                    restaurant=Restaurant.objects.get(name_address1_unique=unique),
                    thumbnail=restaurant_factors['images']['image_0'],
                    category=catetory_name,

                )
            except IntegrityError:
                print('unique 에러여서 넘어감')
                continue


def restaurant_location_create():
    for catetory_name, restaurant_name in detail_page_craw.items():

        for key, restaurant_factors in restaurant_name.items():
            unique = catetory_name + restaurant_factors['title'].replace(" ", "") + restaurant_factors['주소'].replace(
                " ", "")

            print(restaurant_factors['지번'].split()[1])
            try:

                RestaurantLocation.objects.create(
                    restaurant=Restaurant.objects.get(name_address1_unique=unique),
                    location=restaurant_factors['지번'].split()[1],

                )
            except IntegrityError:
                print('unique 에러여서 넘어감')
                continue


def restaurant_images_create():
    for catetory_name, restaurant_name in detail_page_craw.items():

        for key, restaurant_factors in restaurant_name.items():
            unique = catetory_name + restaurant_factors['title'].replace(" ", "") + restaurant_factors['주소'].replace(
                " ", "")

            #         print(restaurant_factors['images'])
            print('\n')
            for image in restaurant_factors['images']:
                print(restaurant_factors['images'][image])

                #         print(aa.name)
                try:

                    RestaurantImages.objects.create(
                        restaurant=Restaurant.objects.get(name_address1_unique=unique),
                        photo=restaurant_factors['images'][image],
                    )
                except IntegrityError:
                    print('unique 에러여서 넘어감')
                    continue


try:
    restaurant_create()
    restaurant_category_create()
    restaurant_location_create()
    restaurant_images_create()

except IntegrityError:
    print('error 발생 모델 생성에')
