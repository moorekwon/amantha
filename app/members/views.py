import requests
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.base import SECRETS
from members.models import *
from members.serializers import *
from members.permissions import IsUserOrReadOnly

User = get_user_model()


class UserStatAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        star = Star.objects.filter(user=request.user)
        print('star >> ', star)
        return Response(f'stat은 {star[0].user.stat}입니다.')


# 해당 유저의 이메일 정보로 상세프로필 정보 불러오기
class UserThroughEmailAPIView(APIView):
    # superuser만 read/write 할 수 있도록 설정 필요!
    permission_classes = [permissions.IsAdminUser, ]

    def post(self, request):
        user = User.objects.get(email=request.data['email'])
        data = {
            'userProfile': UserProfileSerializer(user).data,
        }
        return Response(data)


# 회원가입 (토큰 생성)
class CreateUserAPIView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # 계정 생성 시 리본 기본 지급 (맞는지 모르겠음.. 일단 보류)
            UserRibbon.objects.create(user=user, paid_ribbon=0, current_ribbon=50)
            token = Token.objects.create(user=user)

            data = {
                'token': token.key,
                'user': UserAccountSerializer(user).data,
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # (가입된) 유저 리스트
    def get(self, request):
        users = User.objects.all()
        login = []
        logout = []
        waiting = []
        on_screening = []
        fail = []
        superusers = []

        for user in users:
            # 테스트를 위해 임의 6명 관리자 생성
            if user.is_superuser:
                superusers.append(user.email)
            # 아직 가입심사 전 상태 (가입심사한 이성 0명인 상태)
            elif user.status() == 'waiting':
                waiting.append(user)
            # 가입심사 중인 상태 (가입심사한 이성 1~2명인 상태)
            elif user.status() == 'on_screening':
                on_screening.append(user)
            # 가입심사 불합격 (가입심사한 이성 3명 이상인 상태)
            elif user.status() == 'fail':
                fail.append(user)
            # 가입심사 합격 (가입심사한 이성 3명 이상인 상태)
            else:
                try:
                    # 합격한 유저중 로그인 상태
                    login.append(user.auth_token.user)
                except:
                    # 합격한 유저중 로그아웃 상태
                    logout.append(user)

        data = {
            'superusers': superusers,
            'login': UserAccountSerializer(login, many=True).data,
            'logout': UserAccountSerializer(logout, many=True).data,
            'waiting': UserAccountSerializer(waiting, many=True).data,
            'onScreening': UserAccountSerializer(on_screening, many=True).data,
            'fail': UserAccountSerializer(fail, many=True).data,
        }
        return Response(data)

    # 로그인(토큰 가져오거나 생성)
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        # 유저 인증되고, 가입심사 합격한 유저의 경우
        if user and user.status() == 'pass':
            if not len(user.userribbon_set.all()):
                UserRibbon.objects.create(user=user, paid_ribbon=10, current_ribbon=10)
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed('유저 인증에 성공하지 못하였거나, 가입심사를 합격한 유저가 아닙니다.')

        data = {
            'token': token.key,
            'user': UserAccountSerializer(user).data
        }
        return Response(data)


# 계정 탈퇴
class UserDeleteAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(email=request.user.email)
            user.delete()
            return Response('탈퇴가 완료되었습니다.')
        else:
            raise AuthenticationFailed('유저 인증에 성공하지 못하였습니다.')


# 로그아웃 (토큰 삭제)
class LogoutUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        token = Token.objects.get(user=request.user)

        if not token:
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        token.delete()
        return Response('로그아웃 되었습니다.')


# 유저의 상세프로필 전체 정보 가져오기
class UserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        if Token.objects.filter(user=request.user):
            data = {
                'userProfile': UserProfileSerializer(request.user).data,
            }
            return Response(data)
        # 로그아웃된 유저도 정보 볼 수 있도록 해야하는지 확인필요
        return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')


class UserImageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # user 프로필 이미지 갖고오기
    def get(self, request):
        images = UserImage.objects.filter(user=request.user)
        serializer = UserImageSerializer(images, many=True)

        data = {
            'images': serializer.data,
        }
        return JsonResponse(data, safe=False)

    # user 프로필 이미지 추가하기
    # 계정 생성 시 꼭 3개 추가해야 함
    def post(self, request):
        images = request.data.getlist('images')

        arr = []
        for image in images:
            data = {
                'image': image,
            }
            serializer = UserImageSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                arr.append(serializer.data)
            else:
                return Response(serializer.errors)

        data = {
            'images': arr,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    # user 프로필 이미지 삭제하기
    def delete(self, request, pk):
        images = UserImage.objects.filter(user=request.user)
        if len(images) <= 3:
            return Response('최소 3장 이상 업로드돼있어야 합니다.')

        image = UserImage.objects.filter(user=request.user, pk=pk)
        if image:
            image.delete()
            return Response('해당 이미지가 삭제되었습니다.')
        return Response('해당 이미지의 pk가 존재하지 않습니다.')


class UserInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # 해당 유저의 상세프로필 정보 가져오기
    def get(self, request):
        info = UserInfo.objects.get(user=request.user)

        # 아래 response는 뜨면 안되는 response임..
        # 계정 생성 직후 바로 프로필 정보를 등록해야 함
        if not info:
            return Response('등록된 프로필 정보가 없습니다.')

        data = {
            'info': UserInfoSerializer(info).data,
        }
        return Response(data)

    # (회원가입 직후 첫) 상세프로필 작성 (처음 생성 시 딱 한번 사용)
    def post(self, request):
        info = UserInfo.objects.get(user=request.user)

        # 이미 등록된 프로필 정보가 있으면 안됨..
        # 계정 생성 직후 첫 프로필정보 등록하는 곳
        if info or request.user.status() == 'pass':
            return Response('이미 등록된 프로필 정보가 있습니다.')

        serializer = UserInfoSerializer(data=request.data)

        if serializer.is_valid():
            info = serializer.save(user=request.user)

            data = {
                'info': UserInfoSerializer(info).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 상세프로필 수정
    def patch(self, request):
        info = UserInfo.objects.get(user=request.user)

        if not info or request.user.status() != 'pass':
            return Response('등록된 프로필 정보가 없거나 가입심사를 합격한 유저가 아닙니다.')

        serializer = UserInfoSerializer(info, data=request.data, partial=True)

        if serializer.is_valid():
            info = serializer.save()

            data = {
                'info': UserInfoSerializer(info).data
            }
            return Response(data)
        return Response(serializer.errors)


class UserStoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # 해당 유저의 스토리 불러오기
    def get(self, request):
        stories = Story.objects.filter(user=request.user)

        if not stories:
            return Response('등록된 스토리가 없습니다.')

        serializer = UserStorySerializer(stories, many=True)

        data = {
            'stories': serializer.data,
        }
        return Response(data)

    # 해당 유저의 스토리 추가
    def post(self, request):
        serializer = UserStorySerializer(data=request.data)
        user_stories = request.user.story_set.all()
        user_story_numbers = set()
        # 현재 유저가 등록한 스토리 번호 불러와 저장
        for user_story in user_stories:
            user_story_numbers.add(user_story.story)

        # POST 요청한 스토리 번호가 이미 등록된 스토리일 경우, response 메시지
        if str(request.data['story']) in user_story_numbers:
            return Response('이미 등록되어있는 스토리 입니다.')

        if serializer.is_valid():
            story = serializer.save(user=request.user)

            data = {
                'story': UserStorySerializer(story).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 현재 유저의 등록되어있는 스토리에 접근하여 content 수정
    def patch(self, request):
        story = request.data['story']

        user_stories = Story.objects.filter(user=request.user, story=story)

        if not user_stories:
            return Response('등록되어있지 않은 스토리 입니다.')

        # 아래 코드는 user_stories의 마지막번째를 불러옴
        # 어차피 user_stories는 한 개밖에 없을 것이기 때문에, user_stories[0]을 불러와도 상관은 없을 것임
        serializer = UserStorySerializer(user_stories.last(), data=request.data)

        if serializer.is_valid():
            story = serializer.save()

            data = {
                'story': UserStorySerializer(story).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 스토리 삭제하기
    def delete(self, request, pk):
        story = Story.objects.filter(user=request.user, pk=pk)

        if story:
            story.delete()
            return Response('해당 스토리가 삭제되었습니다.')
        return Response('해당 스토리의 pk가 존재하지 않습니다.')


class UserRibbonAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # User별 보유리본 조회
    def get(self, request):
        ribbons = UserRibbon.objects.filter(user=request.user)

        # 사실 계정 생성과 동시에 유저의 상태와 상관없이 리본 10개 지급되지만, 내역 없다고 response 설정
        if request.user.status() != 'pass':
            return Response('리본 내역이 없습니다.')

        serializer = UserRibbonSerializer(ribbons, many=True)

        data = {
            'ribbonHistory': serializer.data,
        }
        return Response(data)

    def post(self, request):
        if request.user.status() != 'pass':
            return Response('가입심사를 합격한 유저가 아닙니다.')

        if not Token.objects.filter(user=request.user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = UserRibbonSerializer(data=request.data)

        # 보유 리본이 부족할 경우 response
        if request.user.userribbon_set.last().current_ribbon + request.data['paidRibbon'] < 0:
            return Response('보유 리본이 부족합니다.')

        if serializer.is_valid():
            ribbon = serializer.save(user=request.user)

            data = {
                'ribbon': UserRibbonSerializer(ribbon).data,
            }
            return Response(data)
        return Response(serializer.errors)


class UserPickAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # 해당 유저에 해 pick한 이성과 pick받은 이성 조회
    def get(self, request):
        pick_from_users = request.user.send_me_pick_users.all()
        pick_to_users = Pick.objects.filter(user=request.user)

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
            'pickFrom': pick_from_list,
            'pickTo': pick_to_list,
        }
        return Response(data)

    # partner에게 pick 주기
    def post(self, request):
        if request.user.status() != 'pass':
            return Response('가입심사를 합격한 유저가 아닙니다.')

        # partner의 email 정보를 통해 pk에 접근
        partner = User.objects.get(email=request.data['partner'])

        if partner.status() != 'pass':
            return Response('가입심사를 합격한 이성이 아닙니다.')

        if request.user in partner.send_me_pick_users.all():
            return Response('이미 pick한 이성 입니다.')

        data = {
            'user': request.user.pk,
            'partner': partner.pk,
        }

        serializer = UserPickSerializer(data=data)

        if serializer.is_valid():
            like_true = serializer.save()
            return Response(UserPickSerializer(like_true).data)
        return Response(serializer.errors)


class UserStarAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # 가입심사 보낸 이성과 받은 이성 리스트 및 해당 유저의 평균 별점 조회
    def get(self, request):
        stars_from = request.user.send_me_star_users.all()
        stars_to = Star.objects.filter(user=request.user)

        stars_from_list = list()
        for star_from in stars_from:
            # 가입심사 한 이성의 email 값과 이성이 준 별점을 tuple 형태로 추가
            stars_from_list.append(
                (star_from.email, Star.objects.filter(user=star_from, partner=request.user)[0].star)
            )

        stars_to_list = list()
        for star_to in stars_to:
            # 가입심사 받은 이성의 email 값과 이성에게 준 별점을 tuple 형태로 추가
            stars_to_list.append(
                (star_to.partner.email, Star.objects.filter(user=request.user, partner=star_to.partner)[0].star)
            )

        data = {
            'starTo': stars_to_list,
            'starFrom': stars_from_list,
        }
        return Response(data)

    def post(self, request):
        if request.user.status() != 'pass':
            return Response('가입심사를 통과한 유저가 아닙니다.')

        if not Token.objects.filter(user=request.user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        # partner의 email 정보를 통해 pk에 접근
        partner = User.objects.get(email=request.data['partner'])

        # 넣지 않아도 되는지 확인 필요!
        if partner.status() == 'fail':
            return Response('이미 가입심사를 불합격한 이성입니다.')

        star = request.data['star']

        if request.user in partner.send_me_star_users.all():
            return Response('이미 가입심사한 이성 입니다.')

        data = {
            'partner': partner.pk,
            'star': star,
        }

        serializer = UserStarSerializer(data=data)

        if serializer.is_valid():
            star = serializer.save()
            return Response(UserStarSerializer(star).data)
        return Response(serializer.errors)

    # 가입심사한 이성 재심사 (일단 재심사 안하기로 함)
    # def patch(self, request):
    #     if not Token.objects.filter(user=request.user):
    #         return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')
    #
    #     partners = request.user.user_star_set.all()
    #     star = request.data['star']
    #
    #     for partner in partners:
    #         if not partner.partner.email == request.data['partner']:
    #             return Response('가입심사한 적 없는 이성입니다.')
    #         else:
    #             data = {
    #                 'user': request.user.pk,
    #                 'partner': partner.partner.pk,
    #                 'star': star
    #             }
    #             serializer = UserStarSerializer(partner, data=data)
    #
    #             if serializer.is_valid():
    #                 stars = serializer.save()
    #                 return Response(UserStarSerializer(stars).data)
    #             return Response(serializer.errors)


class UserIdealTypeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # 해당 유저의 현재 이상형 설정 정보 조회와 맞춤 이성 소개
    def get(self, request):
        user = request.user
        ideal_type = UserIdealType.objects.filter(user=user)

        if not ideal_type:
            return Response('등록된 이상형 정보가 없습니다.')

        if user.gender == '여자':
            partner_gender = '남자'
        else:
            partner_gender = '여자'

        # 해당 유저와 성별이 다른 이성들 필터링
        partners = User.objects.filter(gender=partner_gender)

        # ideal_partners에 이상형 조건이 (하나라도) 포함된 이성 저장
        ideal_partners = list()

        # 선호지역2가 있어서 나머지 정보는 2번 넣고, 선호지역2만 1번 넣는걸로 일단 설정..
        for partner in partners:
            if user.useridealtype_set.last().age_from and (
                    partner.age() >= user.useridealtype_set.last().age_from) and (
                    partner.age() <= user.useridealtype_set.last().age_to):
                ideal_partners.append(partner)
                ideal_partners.append(partner)
            print('ideal_partners age >> ', ideal_partners)

            if user.useridealtype_set.last().region and (
                    partner.userinfo.region == user.useridealtype_set.last().region):
                ideal_partners.append(partner)
                ideal_partners.append(partner)
            print('ideal_partners region >> ', ideal_partners)

            if user.useridealtype_set.last().region and (
                    partner.userinfo.region == user.useridealtype_set.last().region2):
                ideal_partners.append(partner)

            if user.useridealtype_set.last().tall_from and partner.userinfo.tall and (
                    partner.userinfo.tall >= user.useridealtype_set.last().tall_from) and (
                    partner.userinfo.tall <= user.useridealtype_set.last().tall_to):
                ideal_partners.append(partner)
                ideal_partners.append(partner)
            print('ideal_partners tall >> ', ideal_partners)

            if user.useridealtype_set.last().body_shape and (
                    partner.userinfo.body_shape == user.useridealtype_set.last().body_shape):
                ideal_partners.append(partner)
            print('ideal_partners body >> ', ideal_partners)

            if user.useridealtype_set.last().personality:
                for personality in user.useridealtype_set.last().personality:
                    if personality in partner.userinfo.personality:
                        ideal_partners.append(partner)
                        ideal_partners.append(partner)
            print('ideal_partners personality >> ', ideal_partners)

            if user.useridealtype_set.last().religion and (
                    partner.userinfo.religion == user.useridealtype_set.last().religion):
                ideal_partners.append(partner)
                ideal_partners.append(partner)
            print('ideal_partners religion >> ', ideal_partners)

            if user.useridealtype_set.last().smoking and (
                    partner.userinfo.smoking == user.useridealtype_set.last().smoking):
                ideal_partners.append(partner)
                ideal_partners.append(partner)
            print('ideal_partners smoking >> ', ideal_partners)

            if user.useridealtype_set.last().drinking and (
                    partner.userinfo.drinking == user.useridealtype_set.last().drinking):
                ideal_partners.append(partner)
                ideal_partners.append(partner)
            print('ideal_partners drinking >> ', ideal_partners)

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

            data = {
                'idealPartners': best_partners,
            }
            return Response(data)
        else:
            data = {
                'idealPartners': '없음',
            }
            return Response(data)

    # (첫) 이상형 정보 설정
    def post(self, request):
        if not Token.objects.filter(user=request.user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        if request.user.status() != 'pass':
            return Response('가입심사를 합격한 유저가 아닙니다.')

        ideal_type = UserIdealType.objects.filter(user=request.user)
        if ideal_type:
            return Response('이미 등록한 이상형 정보가 있습니다.')

        serializer = IdealTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            ideal_type = serializer.save(user=request.user)
            data = {
                'idealTypeInfo': IdealTypeSerializer(ideal_type).data,
            }
            return Response(data)
        return Response(serializer.errors)

    # 등록돼 있는 이상형 정보 수정
    def patch(self, request):
        if request.user.status() != 'pass':
            return Response('가입심사를 합격한 유저가 아닙니다.')

        if not Token.objects.filter(user=request.user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        ideal_type = UserIdealType.objects.filter(user=request.user)

        if not ideal_type:
            return Response('등록된 이상형 정보가 없습니다.')

        # 현재는 기존 저장된 데이터는 수정되지 않으면 그대로 저장되도록 설정 (partial=True)
        serializer = IdealTypeSerializer(ideal_type.last(), data=request.data, partial=True)

        if serializer.is_valid():
            ideal_type = serializer.save()

            data = {
                'idealTypeInfo': IdealTypeSerializer(ideal_type).data,
            }
            return Response(data)
        return Response(serializer.errors)


class UserTagAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # 해당 유저의 모든 관심태그 조회
    def get(self, request):
        if request.user.tag is None:
            request.user.tag = TagType.objects.create()
            request.user.save()

        data = {
            'tags': TagTypeSerializer(request.user.tag).data,
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
    permission_classes = [permissions.IsAuthenticated, ]

    # 데이트 스타일 관심태그 추가
    def patch(self, request):
        if not Token.objects.filter(user=request.user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = TagTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            tags = []
            update_tags = serializer.validated_data.pop('date_style_tag')

            for update_tag in update_tags:
                tags.append(Tag.objects.get_or_create(**update_tag)[0])

            if request.user.tag is None:
                request.user.tag = TagType.objects.create()
                request.user.save()

            request.user.tag.date_style_tag.set(tags)
            return Response(TagTypeSerializer(request.user.tag).data)
        return Response(serializer.errors)


class UserTagLifeStyleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    # 라이프 스타일 관심태그 수정
    # 기존 등록된 관심태그에서 추가되고 삭제되는 것이 아니라, request.data로 타입별 태그 전체 수정
    def patch(self, request):
        if not Token.objects.filter(user=request.user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = TagTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            tags = []
            update_tags = serializer.validated_data.pop('life_style_tag')

            for update_tag in update_tags:
                tags.append(Tag.objects.get_or_create(**update_tag)[0])

            if request.user.tag is None:
                request.user.tag = TagType.objects.create()
                request.user.save()

            request.user.tag.life_style_tag.set(tags)
            return Response(TagTypeSerializer(request.user.tag).data)
        return Response(serializer.errors)


class UserTagCharmAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def patch(self, request):
        if not Token.objects.filter(user=request.user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = TagTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            tags = []
            update_tags = serializer.validated_data.pop('charm_tag')

            for update_tag in update_tags:
                tags.append(Tag.objects.get_or_create(**update_tag)[0])

            if request.user.tag is None:
                request.user.tag = TagType.objects.create()
                request.user.save()

            request.user.tag.charm_tag.set(tags)
            return Response(TagTypeSerializer(request.user.tag).data)
        return Response(serializer.errors)


class UserTagRelationshipAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def patch(self, request):
        if not Token.objects.filter(user=request.user):
            return Response('인증 토큰이 없는 유저입니다. 로그인이 되어있습니까?')

        serializer = TagTypeSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            tags = []
            update_tags = serializer.validated_data.pop('relationship_style_tag')

            for update_tag in update_tags:
                tags.append(Tag.objects.get_or_create(**update_tag)[0])

            if request.user.tag is None:
                request.user.tag = TagType.objects.create()
                request.user.save()

            request.user.tag.relationship_style_tag.set(tags)
            return Response(TagTypeSerializer(request.user.tag).data)
        return Response(serializer.errors)


# 테마 소개
class UserThemaAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        if request.user.status() != 'pass':
            return Response('가입심사를 합격한 유저가 아닙니다.')

        # 해당 유저가 여자일 경우, 남자 테마별 이성 소개
        if request.user.gender == '여자':
            partners = User.objects.filter(gender='남자')

            neither_drinks_nor_smokes = list()
            four_years_older = list()
            over_180_tall = list()
            church_men = list()

            for partner in partners:
                # 술담배를 멀리하는 남자
                if (partner.userinfo.drinking == '마시지 않음') and (partner.userinfo.smoking == '비흡연'):
                    neither_drinks_nor_smokes.append(partner.email)

                # 성숙한 매력의 4살연상
                if partner.age() == (request.user.age() + 4):
                    four_years_older.append(partner.email)

                # 키 180cm 이상의 훈남
                if partner.userinfo.tall and (partner.userinfo.tall >= 180):
                    over_180_tall.append(partner.email)

                # 다정다감한 교회오빠
                if partner.userinfo.religion == '기독교':
                    church_men.append(partner.email)

            data = {
                'neitherDrinksNorSmokes': neither_drinks_nor_smokes,
                'fourYearsOlder': four_years_older,
                'over180Tall': over_180_tall,
                'churchMen': church_men,
            }
            return Response(data)

        # 해당 유저가 남자일 경우, 여자 테마별 이성 소개
        else:
            partners = User.objects.filter(gender='여자')

            over_167_tall = list()
            four_years_younger = list()
            neither_drinks_nor_smokes = list()
            cute_women = list()

            # 테마별 알고리즘 추가
            for partner in partners:
                # 167cm 이상 큰 키의 그녀
                if partner.userinfo.tall and (partner.userinfo.tall >= 167):
                    over_167_tall.append(partner.email)

                # 궁합도 안보는 4살연하
                if partner.age() == (request.user.age() - 4):
                    four_years_younger.append(partner.email)

                # 술담배를 멀리하는 그녀
                if (partner.userinfo.drinking == '마시지 않음') and (partner.userinfo.smoking == '비흡연'):
                    neither_drinks_nor_smokes.append(partner.email)

                # 귀여운 매력의 그녀
                if '귀여운' in partner.userinfo.personality:
                    cute_women.append(partner.email)

            data = {
                'over167Tall': over_167_tall,
                'fourYearsYounger': four_years_younger,
                'neitherDrinksNorSmokes': neither_drinks_nor_smokes,
                'cuteWomen': cute_women,
            }
            return Response(data)


# 유저에게 높은 점수를 준 이성(받은 표현)과 유저가 높은 점수를 준 이성(보낸 표현) 리스트 조회
class UserExpressionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        if request.user.status() != 'pass':
            return Response('가입심사를 합격한 유저가 아닙니다.')

        received_partners = request.user.partner_star_set.all()
        sent_partners = request.user.user_star_set.all()

        received_high_partners = list()
        for partner in received_partners:
            if partner.star >= 4:
                received_high_partners.append(partner.user.email)
        print('received_high_partners >> ', received_high_partners)

        sent_high_partners = list()
        for partner in sent_partners:
            if partner.star >= 4:
                sent_high_partners.append(partner.partner.email)
        print('sent_high_partners >> ', sent_high_partners)

        data = {
            'ReceivedPartners': received_high_partners,
            'SentPartners': sent_high_partners,
        }
        return Response(data)


# 카카오톡 로그인 페이지
def KaKaoTemplate(request):
    return render(request, 'kakao.html')


# 카카오톡 로그인
class KaKaoLoginAPIView(APIView):
    # iOS 부분
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
    #    request.     'client_id': app_key,
    #         'redirect_uri': SECRETS['KAKAO_REDIRECT_URI'],
    #         'code': kakao_access_code,
    #     }
    #
    #     kakao_response = requests.post(url, headers=headers, data=data)
    #     return Response(f'{kakao_response.text}')

    # 액세스 토큰 받아 가입 혹은 로그인 처리
    def post(self, request):
        access_token = request.data['accessToken']
        gender = request.data['gender']
        me_url = SECRETS['KAKAO_ME_URL']
        me_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-type': SECRETS['KAKAO_CONTENT_TYPE'],
        }
        me_response = requests.get(me_url, headers=me_headers)
        me_response_data = me_response.json()
        print('me_response_data >> ', me_response_data)

        # 카카오톡 계정의 이메일로 user의 email 생성
        kakao_email = me_response_data['kakao_account']['email']

        if not User.objects.filter(email=kakao_email).exists():
            user = User.objects.create_user(email=kakao_email, gender=gender)
            token = Token.objects.create(user=user)
        else:
            user = User.objects.get(email=kakao_email, gender=gender)
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
