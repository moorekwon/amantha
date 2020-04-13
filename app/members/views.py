import requests
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import TagType
from members.serializers import *

User = get_user_model()


# 회원가입 (토큰 생성)
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # 계정 생성 시 리본 기본 지급
            UserRibbon.objects.create(user=user, paid_ribbon=10, current_ribbon=10)

            token = Token.objects.create(user=user)

            data = {
                'token': token.key,
                'user': UserAccountSerializer(user).data,
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenAPIView(APIView):
    # (가입된) 유저 리스트
    def get(self, request):
        users = User.objects.all()
        login = []
        logout = []

        for user in users:
            try:
                login.append(user.auth_token.user)
            except:
                logout.append(user)

        data = {
            'login': UserAccountSerializer(login, many=True).data,
            'logout': UserAccountSerializer(logout, many=True).data,
        }
        return Response(data)

    # 로그인(토큰 가져오거나 생성)
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user:
            # createsuperuser 경우, 로그인 시 리본 기본 지급 설정
            # superuser는 로그인 POST 하기 전까지 logout 상태 (자동 로그인 x)
            if not len(user.userribbon_set.all()):
                UserRibbon.objects.create(user=user, paid_ribbon=10, current_ribbon=10)
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed('존재하지 않는 email 입니다.')

        data = {
            'token': token.key,
            'user': UserAccountSerializer(user).data
        }
        return Response(data)


# 로그아웃 (토큰 삭제)
class LogoutUserAPIView(APIView):
    def get(self, request):
        user = request.user
        token = Token.objects.filter(user=user)

        if not token:
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        token.delete()
        return Response('로그아웃 되었습니다.')


# 유저의 상세프로필 전체 정보 가져오기
class UserProfileAPIView(APIView):
    def get(self, request):
        user = request.user

        if Token.objects.filter(user=user):
            data = {
                'userProfile': UserProfileSerializer(user).data,
            }
            return Response(data)
        return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')


class UserImageAPIView(APIView):
    # user 프로필 이미지 갖고오기
    def get(self, request):
        user = request.user
        images = UserImage.objects.filter(user=user)
        serializer = UserImageSerializer(images, many=True)

        data = {
            'user': UserAccountSerializer(user).data,
            'images': serializer.data,
        }
        return JsonResponse(data, safe=False)

    # user 프로필 이미지 추가하기
    def post(self, request):
        user = request.user
        images = request.data.getlist('images')

        arr = []
        for image in images:
            data = {
                'image': image,
            }
            serializer = UserImageSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=user)
                arr.append(serializer.data)
            else:
                return Response(serializer.errors)

        data = {
            'images': arr,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    # user 프로필 이미지 삭제하기
    def delete(self, request, pk):
        user = request.user
        image = UserImage.objects.filter(user=user, pk=pk)
        if image:
            image.delete()
            return Response('해당 이미지가 삭제되었습니다.')
        return Response('해당 이미지의 pk가 존재하지 않습니다.')


class UserInfoAPIView(APIView):
    # 해당 유저의 상세프로필 정보 가져오기
    def get(self, request):
        user = request.user
        info = UserInfo.objects.filter(user=user)

        if not info:
            return Response('등록된 프로필 정보가 없습니다.')

        data = {
            'user': UserAccountSerializer(user).data,
            'info': UserInfoSerializer(info[0]).data,
        }
        return Response(data)

    # (회원가입 직후 첫) 상세프로필 작성 (처음 생성 시 딱 한번 사용)
    def post(self, request):
        user = request.user
        info = UserInfo.objects.filter(user=user)

        if info:
            return Response('이미 등록된 프로필 정보가 있습니다.')

        serializer = UserInfoSerializer(data=request.data)

        if serializer.is_valid():
            info = serializer.save(user=user)

            data = {
                'info': UserInfoSerializer(info).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 상세프로필 수정
    def patch(self, request):
        info = UserInfo.objects.filter(user=request.user)

        if not info:
            return Response('등록된 프로필 정보가 없습니다. 프로필을 생성해 주세요.')

        serializer = UserInfoSerializer(info[0], data=request.data, partial=True)

        if serializer.is_valid():
            info = serializer.save()

            data = {
                'info': UserInfoSerializer(info).data
            }
            return Response(data)
        return Response(serializer.errors)


class UserStoryAPIView(APIView):
    # 해당 유저의 스토리 불러오기
    def get(self, request):
        user = request.user
        stories = SelectStory.objects.filter(user=user)

        if not stories:
            return Response('등록된 스토리가 없습니다.')

        serializer = UserStorySerializer(stories, many=True)

        data = {
            'user': UserAccountSerializer(user).data,
            'stories': serializer.data,
        }
        return Response(data)

    # 해당 유저의 스토리 추가
    def post(self, request):
        user = request.user
        serializer = UserStorySerializer(data=request.data)

        user_stories = user.selectstory_set.all()
        user_story_numbers = set()
        # 현재 유저가 등록한 스토리 번호 불러와 저장
        for user_story in user_stories:
            user_story_numbers.add(user_story.story)

        # POST 요청한 스토리 번호가 이미 등록된 스토리일 경우, response 메시지
        if str(request.data['story']) in user_story_numbers:
            return Response('이미 등록되어있는 스토리 입니다.')

        if serializer.is_valid():
            story = serializer.save(user=user)

            data = {
                'story': UserStorySerializer(story).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 현재 유저의 등록되어있는 스토리에 접근하여 content 수정
    def patch(self, request):
        user = request.user
        story = request.data['story']

        user_stories = SelectStory.objects.filter(user=user, story=story)

        if not user_stories:
            return Response('등록되어있지 않은 스토리 입니다.')

        # 아래 코드는 user_stories의 마지막번째를 불러옴
        # 어차피 user_stories는 한 개밖에 없을 것이기 때문에, user_stories[0]을 불러와도 상관은 없을 것임
        serializer = UserStorySerializer(user_stories[len(user_stories) - 1], data=request.data)

        if serializer.is_valid():
            story = serializer.save()

            data = {
                'story': UserStorySerializer(story).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 스토리 삭제하기
    def delete(self, request, pk):
        user = request.user
        story = SelectStory.objects.filter(user=user, pk=pk)

        if story:
            story.delete()
            return Response('해당 스토리가 삭제되었습니다.')
        return Response('해당 스토리의 pk가 존재하지 않습니다.')


class UserRibbonAPIView(APIView):
    # User별 보유리본 조회
    def get(self, request):
        user = request.user
        token = Token.objects.filter(user=user)

        if not token:
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        ribbons = UserRibbon.objects.filter(user=user)

        serializer = UserRibbonSerializer(ribbons, many=True)

        data = {
            'user': UserAccountSerializer(user).data,
            'ribbons': serializer.data,
        }
        return Response(data)

    def post(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = UserRibbonSerializer(data=request.data)

        # 보유 리본이 부족할 경우 response
        if user.userribbon_set.last().current_ribbon + request.data['paidRibbon'] < 0:
            return Response('보유 리본이 부족합니다.')

        if serializer.is_valid():
            ribbon = serializer.save(user=user)

            data = {
                'ribbon': UserRibbonSerializer(ribbon).data,
            }
            return Response(data)
        return Response(serializer.errors)


class UserPickAPIView(APIView):
    # 해당 유저에 해 pick한 이성과 pick받은 이성 조회
    def get(self, request):
        user = request.user
        pick_from_users = user.send_me_pick_users.all()
        pick_to_users = SendPick.objects.filter(user=user)

        # 해당 유저가 pick받은 이성들
        pick_from_list = list()
        for pick_from_user in pick_from_users:
            # pick받은 이성들의 email 정보를 표대시
            pick_from_list.append(pick_from_user.email)

        # 해당 유저가 pick한 이성들
        pick_to_list = list()
        for pick_to_user in pick_to_users:
            pick_to_list.append(pick_to_user.partner.email)

        data = {
            'user': UserAccountSerializer(user).data,
            'pickFrom': pick_from_list,
            'pickTo': pick_to_list,
        }
        return Response(data)

    # partner에게 like 주기
    def post(self, request):
        user = request.user
        # partner의 email 정보를 통해 pk에 접근
        partner = User.objects.get(email=request.data['partner'])

        if user in partner.send_me_pick_users.all():
            return Response('이미 pick한 이성 입니다.')

        data = {
            'user': user.pk,
            'partner': partner.pk,
        }

        serializer = UserPickSerializer(data=data)

        if serializer.is_valid():
            like_true = serializer.save()
            return Response(UserPickSerializer(like_true).data)
        return Response(serializer.errors)


class UserStarAPIView(APIView):
    # 가입심사 보낸 이성과 받은 이성 리스트 조회
    def get(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        stars_from = user.send_me_star_users.all()
        stars_to = SendStar.objects.filter(user=user)

        stars_from_list = list()
        for star_from in stars_from:
            # 가입심사 한 이성의 email 값과 이성이 준 별점을 tuple 형태로 추가
            stars_from_list.append(
                (star_from.email, SendStar.objects.filter(user=star_from, partner=user)[0].star)
            )

        stars_to_list = list()
        for star_to in stars_to:
            # 가입심사 받은 이성의 email 값과 이성에게 준 별점을 tuple 형태로 추가
            stars_to_list.append(
                (star_to.partner.email, SendStar.objects.filter(user=user, partner=star_to.partner)[0].star)
            )

        data = {
            'user': UserAccountSerializer(user).data,
            'StarTo': stars_to_list,
            'StarFrom': stars_from_list,
        }
        return Response(data)

    def post(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        # partner의 email 정보를 통해 pk에 접근
        partner = User.objects.get(email=request.data['partner'])
        star = request.data['star']

        if user in partner.send_me_star_users.all():
            return Response('이미 가입심사한 이성 입니다.')

        data = {
            'user': user.pk,
            'partner': partner.pk,
            'star': star,
        }

        serializer = UserStarSerializer(data=data)

        if serializer.is_valid():
            star = serializer.save()
            return Response(UserStarSerializer(star).data)
        return Response(serializer.errors)


class UserIdealTypeAPIView(APIView):
    # 해당 유저의 현재 이상형 설정 정보 불러오기
    def get(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        ideal_type = UserIdealType.objects.filter(user=user)
        print('ideal_type >> ', ideal_type)

        if not ideal_type:
            return Response('등록된 이상형 정보가 없습니다.')

        data = {
            'user': UserAccountSerializer(user).data,
            'idealType': IdealTypeSerializer(ideal_type.last()).data,
        }
        return Response(data)

    # (첫) 이상형 설정하여 맞춤 이성 추천받기
    def post(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        # ideal_type = UserIdealType.objects.filter(user=user)
        # if ideal_type:
        #     return Response('이미 등록한 이상형 정보가 있습니다.')

        if user.gender == '여자':
            partner_gender = '남자'
        else:
            partner_gender = '여자'

        # 해당 유저와 성별이 다른 이성들 필터링
        partners = User.objects.filter(gender=partner_gender)

        serializer = IdealTypeSerializer(data=request.data, partial=True)
        print('serializer >> ', serializer)

        # ideal_partners에 이상형 조건이 (하나라도) 포함된 이성 저장
        ideal_partners = list()

        for partner in partners:
            if (request.data.get('ageFrom') is not None) and (partner.age() >= request.data.get('ageFrom')) and (
                    partner.age() <= request.data['ageTo']):
                ideal_partners.append(partner)
            print('ideal_partners age >> ', ideal_partners)

            if (request.data.get('region') is not None) and (partner.userinfo.region is not None) and (
                    partner.userinfo.region == request.data['region']):
                ideal_partners.append(partner)
            print('ideal_partners region >> ', ideal_partners)

            if (request.data.get('tallFrom') is not None) and (partner.userinfo.tall is not None) and (
                    partner.userinfo.tall >= request.data['tallFrom']) and (
                    partner.userinfo.tall <= request.data['tallTo']):
                ideal_partners.append(partner)
            print('ideal_partners tall >> ', ideal_partners)

            if (request.data.get('bodyShape') is not None) and (partner.userinfo.body_shape is not None) and (
                    partner.userinfo.body_shape == request.data['bodyShape']):
                ideal_partners.append(partner)
            print('ideal_partners body >> ', ideal_partners)

            if (request.data.get('religion') is not None) and (partner.userinfo.religion is not None) and (
                    partner.userinfo.religion == request.data['religion']):
                ideal_partners.append(partner)
            print('ideal_partners religion >> ', ideal_partners)

            if (request.data.get('smoking') is not None) and (partner.userinfo.smoking is not None) and (
                    partner.userinfo.smoking == request.data['smoking']):
                ideal_partners.append(partner)
            print('ideal_partners smoking >> ', ideal_partners)

            if (request.data.get('drinking') is not None) and (partner.userinfo.drinking is not None) and (
                    partner.userinfo.drinking == request.data['drinking']):
                ideal_partners.append(partner)
            print('ideal_partners drinking >> ', ideal_partners)
        print('ideal_partners >> ', ideal_partners)

        # better_partners에 포함된 이성들의 중복 횟수 저장 (많을수록 better)
        better_partners = dict()
        for ideal_partner in ideal_partners:
            try:
                better_partners[ideal_partner] += 1
            except:
                better_partners[ideal_partner] = 1
        print('better_partners >> ', better_partners)

        if better_partners:
            max_count = max(better_partners.values())

            # best_partners에 횟수가 가장 많은 이성 저장
            best_partners = list()
            for key, value in better_partners.items():
                if value == max_count:
                    best_partners.append(key.email)
            print('best_partners >> ', best_partners)

            if serializer.is_valid():
                ideal_type = serializer.save(user=user)
                data = {
                    'idealType': IdealTypeSerializer(ideal_type).data,
                    'idealPartners': best_partners,
                }
                return Response(data)
            return Response(serializer.errors)
        else:
            return Response('설정하신 이상형 정보와 매칭되는 이성이 없습니다.')

    # 등록돼 있는 이상형 정보 수정
    def patch(self, request):
        pass


class UserTagAPIView(APIView):
    # 해당 유저의 모든 관심태그 조회
    def get(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        # TagType.objects.get_or_create(user=user)
        if user.tag is None:
            user.tag = TagType.objects.create()
            user.save()

        print('user.tag >> ', user.tag)

        data = {
            'user': UserAccountSerializer(user).data,
            'tags': TagTypeSerializer(user.tag).data,
        }
        return Response(data)

    # 현재 작동 안됨.! (태그타입별로 api 넣지 않고 한꺼번에 partial update 시도했으나 실패..)
    # def patch(self, request):
    #     user = request.user
    #     serializer = TagTypeSerializer(data=request.data, partial=True)
    #     print('serializer >> ', serializer)
    #
    #     if serializer.is_valid():
    #         print('valid!')
    #         date_style_tags = []
    #         life_style_tags = []
    #         charm_tags = []
    #         relationship_style_tags = []
    #
    #         if request.data['dateStyle']:
    #             update_date_tags = serializer.validated_data.pop('date_style_tag')
    #
    #             for update_date_tag in update_date_tags:
    #                 date_style_tags.append(Tag.objects.get_or_create(**update_date_tag[0]))
    #         print('date_style_tags >> ', date_style_tags)
    #         user.date_style_tag.set(date_style_tags)
    #
    #         if request.data['lifeStyle']:
    #             update_life_tags = serializer.validated_data.pop('life_style_tag')
    #
    #             for update_life_tag in update_life_tags:
    #                 life_style_tags.append(Tag.objects.get_or_create(**update_life_tag[0]))
    #         user.life_style_tag.set(life_style_tags)
    #         print('life_style_tags >> ', life_style_tags)
    #
    #         if request.data['charm']:
    #             update_charm_tags = serializer.validated_data.pop('charm_tag')
    #
    #             for update_charm_tag in update_charm_tags:
    #                 charm_tags.append(Tag.objects.get_or_create(**update_charm_tag[0]))
    #         user.charm_tag.set(charm_tags)
    #         print('charm_tags >> ', charm_tags)
    #
    #         if request.data['relationshipStyle']:
    #             update_relationship_tags = serializer.validated_data.pop('relathionship_style_tag')
    #
    #             for update_relationship_tag in update_relationship_tags:
    #                 relationship_style_tags.append(Tag.objects.get_or_create(**update_relationship_tag[0]))
    #         user.relationship_style_tag.set(relationship_style_tags)
    #         print('relationship_style_tags >> ', relationship_style_tags)
    #
    #         return Response(TagTypeSerializer(user).data)
    #     return Response(serializer.errors)


class UserTagDateStyleAPIView(APIView):
    # 데이트 스타일 관심태그 추가
    def patch(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = TagTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            tags = []
            update_tags = serializer.validated_data.pop('date_style_tag')

            for update_tag in update_tags:
                tags.append(Tag.objects.get_or_create(**update_tag)[0])

            if user.tag is None:
                user.tag = TagType.objects.create()
                user.save()

            user.tag.date_style_tag.set(tags)
            return Response(TagTypeSerializer(user.tag).data)
        return Response(serializer.errors)


class UserTagLifeStyleAPIView(APIView):
    # 라이프 스타일 관심태그 수정
    # 기존 등록된 관심태그에서 추가되고 삭제되는 것이 아니라, request.data로 타입별 태그 전체 수정
    def patch(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = TagTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            tags = []
            update_tags = serializer.validated_data.pop('life_style_tag')

            for update_tag in update_tags:
                tags.append(Tag.objects.get_or_create(**update_tag)[0])

            if user.tag is None:
                user.tag = TagType.objects.create()
                user.save()

            user.tag.life_style_tag.set(tags)
            return Response(TagTypeSerializer(user.tag).data)
        return Response(serializer.errors)


class UserTagCharmAPIView(APIView):
    def patch(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = TagTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            tags = []
            update_tags = serializer.validated_data.pop('charm_tag')

            for update_tag in update_tags:
                tags.append(Tag.objects.get_or_create(**update_tag)[0])

            if user.tag is None:
                user.tag = TagType.objects.create()
                user.save()

            user.tag.charm_tag.set(tags)
            return Response(TagTypeSerializer(user.tag).data)
        return Response(serializer.errors)


class UserTagRelationshipAPIView(APIView):
    def patch(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = TagTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            tags = []
            update_tags = serializer.validated_data.pop('relationship_style_tag')

            for update_tag in update_tags:
                tags.append(Tag.objects.get_or_create(**update_tag)[0])

            if user.tag is None:
                user.tag = TagType.objects.create()
                user.save()

            user.tag.relationship_style_tag.set(tags)
            return Response(TagTypeSerializer(user.tag).data)
        return Response(serializer.errors)


# 카카오톡 로그인 페이지
def KaKaoTemplate(request):
    return render(request, 'kakao.html')

# 카카오톡 로그인
# class KaKaoLoginAPIView(APIView):
# # iOS 부분
# def get(self, request):
#     app_key = SECRETS['KAKAO_APP_KEY']
#     kakao_access_code = request.GET.get('code', None)
#     url = SECRETS['KAKAO_URL']
#     headers = {
#         'Content-type': SECRETS['KAKAO_CONTENT_TYPE']
#     }
#
#     data = {
#         'grant_type': 'authorization_code',
#         'client_id': app_key,
#         'redirect_uri': SECRETS['KAKAO_REDIRECT_URI'],
#         'code': kakao_access_code,
#     }
#
#     kakao_response = requests.post(url, headers=headers, data=data)
#     return Response(f'{kakao_response.text}')

# 액세스 토큰 받아 가입 혹은 로그인 처리
# def post(self, request):
#     access_token = request.data['accessToken']
#     gender = request.data['gender']
#     me_url = SECRETS['KAKAO_ME_URL']
#     me_headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-type': SECRETS['KAKAO_CONTENT_TYPE']
#     }
#     me_response = requests.get(me_url, headers=me_headers)
#     me_response_data = me_response.json()
#
#     # 카카오톡 계정의 이메일로 user의 email 생성
#     kakao_email = me_response_data['kakao_account']['email']
#
#     if not User.objects.filter(email=kakao_email).exists():
#         user = User.objects.create_user(email=kakao_email, gender=gender)
#         token = Token.objects.create(user=user)
#     else:
#         user = User.objects.get(email=kakao_email, gender=gender)
#         token, _ = Token.objects.get_or_create(user=user)
#
#     # 카카오톡 계정의 고유 id로 user의 username 생성
#     # kakao_id = me_response_data['id']
#     # kakao_username = f'n_{kakao_id}'
#     #
#     # if not User.objects.filter(username=kakao_username).exists():
#     #     user = User.objects.create_user(username=kakao_username)
#     #     token = Token.objects.create(user=user)
#     # else:
#     #     user = User.objects.get(username=kakao_username)
#     #     token, _ = Token.objects.get_or_create(user=user)
#
#     data = {
#         'user': KakaoUserSerializer(user).data,
#         'token': token.key
#     }
#     return Response(data)
