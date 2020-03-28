from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

# 로그인 (토큰 가져오거나 생성)
from members.serializers import UserSerializer

User = get_user_model()


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

    def get(self, request):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
