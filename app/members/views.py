import requests
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import status, authentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.dev_hj import SECRETS
from members.serializers import UserSerializer, CreateUserSerializer

User = get_user_model()


# 로그인 (토큰 가져오거나 생성)
class AuthTokenAPIView(APIView):
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

    # 유저 리스트
    def get(self, request):
        emails = [user.email for user in User.objects.all()]
        return Response(emails)


# 회원가입 (토큰 생성)
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)

            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃 (토큰 삭제)
class LogoutUserAPIView(APIView):
    def get(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response('로그아웃 되었습니다.')


# 카카오톡 로그인
class KaKaoLoginAPIView(APIView):
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

    def post(self, request):
        access_token = request.data['access_token']
        me_url = SECRETS['KAKAO_ME_URL']
        me_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-type': SECRETS['KAKAO_CONTENT_TYPE']
        }
        me_response = requests.get(me_url, headers=me_headers)
        me_response_data = me_response.json()
        print('me_response_data >> ', me_response_data)

        kakao_email = me_response_data['kakao_account']['email']
        # kakao_gender = me_response_data['kakao_account']['gender']
        # print('kakao_gender >> ', kakao_gender)
        print('kakao_email >> ', kakao_email)

        if not User.objects.filter(email=kakao_email).exists():
            user = User.objects.create_user(email=kakao_email)
            token = Token.objects.create(user=user)
        else:
            user = User.objects.get(email=kakao_email)
            token, _ = Token.objects.get_or_create(user=user)

        data = {
            'user': UserSerializer(user).data,
            'token': token.key
        }
        return Response(data)


def KaKaoTemplate(request):
    return render(request, 'kakao.html')
