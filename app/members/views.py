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
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


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
        print('user >> ', user)
        token = Token.objects.get(user=user)
        token.delete()
        return Response('로그아웃 되었습니다.')
