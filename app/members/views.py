import requests
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.dev_hj import SECRETS
from members.models import UserProfile

from members.serializers import UserSerializer, KakaoUserSerializer, UserProfileSerializer, UserCreateSerializer

User = get_user_model()


# 회원가입 (토큰 생성)
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)

            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ImageListAPIView(APIView):
#     def post(self, request):
#         user = request.user
#         images = user.userimage_set.all()
#
#         serializer = UserImageSerializer(images, context={"request": request})
#         print('serializer >> ', serializer)
#         if serializer.is_valid():
#             serializer.save(user=user)
#
#             return Response(serializer.data)
#         return Response(serializer.errors)


class CreateUserProfileAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    # 상세프로필 생성
    def post(self, request):
        user = request.user
        serializer = UserProfileSerializer(data=request.data)
        print('request.data >> ', request.data)

        if serializer.is_valid():
            user_profile = serializer.save(user=user)

            data = {
                'user_profile': UserProfileSerializer(user_profile).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 상세프로필 수정
    def patch(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            user_profile = serializer.save()

            data = {
                'user_profile': UserProfileSerializer(user_profile).data
            }
            return Response(data)
        return Response(serializer.errors)


class AuthTokenAPIView(APIView):
    # 로그인(토큰 가져오거나 생성)
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        data = {
            'token': token.key,
            'user': UserSerializer(user).data
        }
        return Response(data)

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


# 로그아웃 (토큰 삭제)
class LogoutUserAPIView(APIView):
    def get(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response('로그아웃 되었습니다.')


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
