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


class UserTagAPIView(APIView):
    # 해당 유저의 관심태그 불러오기
    def get(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        # if not user.tags.all():
        #     return Response('등록된 관심태그가 없습니다.')

        # date_style = user.date_style_tag()
        # date_style_name = [date_style.name for date_style in date_style.all()]

        data = {
            'user': UserAccountSerializer(user).data,
            # 'tags': UserTagSerializer(user).data,
        }
        return Response(data)

    # 관심태그 추가(및 변경)
    def post(self, request):
        user = request.user

        if not Token.objects.filter(user=user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        # 처음 관심태그 등록할 경우,
        # if not user.tags.all():
        #     type = request.data['type']
        #     name = request.data['name']
        #
        #     user_tag = user.tags.create(type=type, name=name)
        #     serializer = UserTagSerializer(user_tag, data=request.data, many=True)
        #
        # # 관심태그 추가할 경우, 기존 데이터와 상관없이 해당 KEY값에 대해 request.data로 완전 수정
        # else:
        #     serializer = UserTagSerializer(user.tags, data=request.data, partial=True)
        #
        # if serializer.is_valid():
        #     tag = serializer.save()
        #
        #     data = {
        #         'tags': UserTagSerializer(tag).data,
        #     }
        #     return Response(data)
        # return Response(serializer.errors)
        return 0


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
