import requests
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.dev_hj import SECRETS
from members.models import UserInfo, UserImage, SelectStory

from members.serializers import KakaoUserSerializer, UserProfileSerializer, UserCreateSerializer, \
    UserImageSerializer, UserStorySerializer, UserInfoSerializer, UserSerializer

User = get_user_model()


# 회원가입 (토큰 생성)
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            print('user.is_authenticated >>', user.is_authenticated)

            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
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
            'login': UserSerializer(login, many=True).data,
            'logout': UserSerializer(logout, many=True).data,
        }
        return Response(data)

    # 로그인(토큰 가져오거나 생성)
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed('존재하지 않는 email 입니다.')

        data = {
            'token': token.key,
            'user': UserSerializer(user).data
        }
        return Response(data)


# 로그아웃 (토큰 삭제)
class LogoutUserAPIView(APIView):
    def get(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response('로그아웃 되었습니다.')


class UserImageAPIView(APIView):
    # user 프로필 이미지 갖고오기
    def get(self, request):
        user = request.user
        images = UserImage.objects.filter(user=user)
        serializer = UserImageSerializer(images, many=True)

        data = {
            'user': UserSerializer(user).data,
            'user_image': serializer.data,
        }
        return JsonResponse(data, safe=False)

    # user 프로필 이미지 추가하기
    def post(self, request):
        user = request.user
        images = request.data.getlist('user_image')

        arr = []
        for user_image in images:
            data = {
                'user': UserSerializer(user).data,
                'user_image': user_image,
            }
            serializer = UserImageSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=user)
                arr.append(serializer.data)
            else:
                return Response(serializer.errors)

        data = {
            'user': UserSerializer(user).data,
            'user_image': arr,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserProfileAPIView(APIView):
    # 해당 유저의 상세프로필 정보 가져오기
    def get(self, request):
        user = request.user
        user_info = UserInfo.objects.filter(user=user)

        if not user_info:
            return Response('등록된 프로필 정보가 없습니다.')

        data = {
            'user_profile': UserProfileSerializer(user).data,
        }
        return Response(data)

    # (회원가입 직후 첫) 상세프로필 작성 (처음 생성 시 딱 한번 사용)
    def post(self, request):
        user = request.user

        if user.userinfo:
            return Response('이미 등록된 프로필 정보가 있습니다.')

        serializer = UserInfoSerializer(data=request.data)

        if serializer.is_valid():
            user_info = serializer.save(user=user)

            data = {
                'user_info': UserInfoSerializer(user_info).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 상세프로필 수정
    def patch(self, request):
        user_info = UserInfo.objects.get(user=request.user)
        serializer = UserInfoSerializer(user_info, data=request.data, partial=True)

        if serializer.is_valid():
            user_info = serializer.save()

            data = {
                'user_info': UserInfoSerializer(user_info).data
            }
            return Response(data)
        return Response(serializer.errors)


class UserStoryAPIView(APIView):
    # 해당 유저의 스토리 불러오기
    def get(self, request):
        user = request.user
        story = SelectStory.objects.filter(user=user)

        if not story:
            return Response('등록된 스토리가 없습니다.')

        serializer = UserStorySerializer(story, many=True)

        data = {
            'story': serializer.data,
        }
        return Response(data)

    # 해당 유저의 스토리 추가
    def post(self, request):
        user = request.user
        serializer = UserStorySerializer(data=request.data)

        if serializer.is_valid():
            story = serializer.save(user=user)

            data = {
                'story': UserStorySerializer(story).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 스토리 삭제하기
    def delete(self, request, pk):
        user = request.user
        story = SelectStory.objects.filter(user=user, pk=pk)
        story.delete()
        return Response('해당 스토리가 삭제되었습니다.')


# class UserTagAPIView(APIView):
#     # 해당 유저의 관심태그 불러오기
#     def get(self, request):
#         user = request.user
#         tag = SelectTag.objects.filter(user=user)
#
#         if not tag:
#             return Response('등록된 관심태그가 없습니다.')
#
#         tag = UserTagSerializer(tag, many=True)
#
#         data = {
#             'tag': UserTagSerializer(tag).data,
#         }
#         return Response(data)
#
#     # 관심태그 수정 (multi-check, 기존 데이터와 상관없이 request.data로 완전 수정)
#     def patch(self, request):
#         user = request.user
#         user_tag = SelectTag.objects.get(user=user)
#
#         serializer = UserTagSerializer(user_tag, data=request.data, partial=True)
#         print('serializer.data >>', serializer.is_valid())
#
#         if serializer.is_valid():
#             tag = serializer.save()
#             print('tag >> ', tag)
#
#             data = {
#                 'tag': UserTagSerializer(tag).data,
#             }
#             return Response(data)
#         return Response(serializer.errors)


# 카카오톡 로그인 페이지
def KaKaoTemplate(request):
    return render(request, 'kakao.html')


# 카카오톡 로그인
class KaKaoLoginAPIView(APIView):
    # iOS 부분
    def get(self, request):
        app_key = SECRETS['KAKAO_APP_KEY']
        kakao_access_code = request.GET.get('code', None)
        url = SECRETS['KAKAO_URL']
        headers = {
            'Content-type': SECRETS['KAKAO_CONTENT_TYPE']
        }

        data = {
            'grant_type': 'authorization_code',
            'client_id': app_key,
            'redirect_uri': SECRETS['KAKAO_REDIRECT_URI'],
            'code': kakao_access_code,
        }

        kakao_response = requests.post(url, headers=headers, data=data)
        return Response(f'{kakao_response.text}')

    # 액세스 토큰 받아 가입 혹은 로그인 처리
    def post(self, request):
        access_token = request.data['access_token']
        me_url = SECRETS['KAKAO_ME_URL']
        me_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-type': SECRETS['KAKAO_CONTENT_TYPE']
        }
        me_response = requests.get(me_url, headers=me_headers)
        me_response_data = me_response.json()

        # 카카오톡 계정의 이메일로 user의 email 생성
        kakao_email = me_response_data['kakao_account']['email']

        if not User.objects.filter(email=kakao_email).exists():
            user = User.objects.create_user(email=kakao_email)
            token = Token.objects.create(user=user)
        else:
            user = User.objects.get(email=kakao_email)
            token, _ = Token.objects.get_or_create(user=user)

        # 카카오톡 계정의 고유 id로 user의 username 생성
        # kakao_id = me_response_data['id']
        # kakao_username = f'n_{kakao_id}'
        #
        # if not User.objects.filter(username=kakao_username).exists():
        #     user = User.objects.create_user(username=kakao_username)
        #     token = Token.objects.create(user=user)
        # else:
        #     user = User.objects.get(username=kakao_username)
        #     token, _ = Token.objects.get_or_create(user=user)

        data = {
            'user': KakaoUserSerializer(user).data,
            'token': token.key
        }
        return Response(data)
