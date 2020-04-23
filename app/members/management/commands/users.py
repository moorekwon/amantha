from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from rest_framework.authtoken.models import Token

from members.models import *

User = get_user_model()


class Command(BaseCommand):
    help = '깨끗한 상태의 DB에서 default로 유저 8명을 생성합니다.'

    def handle(self, *args, **kwargs):
        User.objects.create_superuser(email='man1@man.com', password='man1', gender='여자')
        User.objects.create_superuser(email='man2@man.com', password='man2', gender='여자')
        User.objects.create_superuser(email='man3@man.com', password='man3', gender='여자')
        User.objects.create_superuser(email='man4@man.com', password='man4', gender='남자')
        User.objects.create_superuser(email='man5@man.com', password='man5', gender='남자')
        User.objects.create_superuser(email='man6@man.com', password='man6', gender='남자')
        print('6명의 관리자 user가 생성되었습니다.')

        man1 = User.objects.get(email='man1@man.com')
        man2 = User.objects.get(email='man2@man.com')
        man3 = User.objects.get(email='man3@man.com')
        man4 = User.objects.get(email='man4@man.com')
        man5 = User.objects.get(email='man5@man.com')
        man6 = User.objects.get(email='man6@man.com')
        print('6명의 관리자 user들을 변수로 저장하여 불러왔습니다.')

        UserInfo.objects.create(user=man1, nickname='관리자1', birth='1985-01-23', tall=156)
        UserInfo.objects.create(user=man2, nickname='관리자2', birth='1993-01-23', tall=163)
        UserInfo.objects.create(user=man3, nickname='관리자3', birth='1996-01-23', tall=168)
        UserInfo.objects.create(user=man4, nickname='관리자4', birth='1986-01-23', tall=171)
        UserInfo.objects.create(user=man5, nickname='관리자5', birth='1992-01-23', tall=177)
        UserInfo.objects.create(user=man6, nickname='관리자6', birth='1997-01-23', tall=182)
        print('6명의 관리자 프로필정보가 생성되었습니다.')

        User.objects.create_user(email='hjk@hjk.com', password='hjk', gender='여자')
        User.objects.create_user(email='ebk@ebk.com', password='ebk', gender='여자')
        User.objects.create_user(email='szj@szj.com', password='szj', gender='여자')
        User.objects.create_user(email='hbb@hbb.com', password='hbb', gender='남자')
        User.objects.create_user(email='hgo@hgo.com', password='hgo', gender='남자')
        User.objects.create_user(email='dhl@dhl.com', password='dhl', gender='남자')
        print('User 테이블에 6명의 user가 생성되었습니다.')

        hjk = User.objects.get(email='hjk@hjk.com')
        ebk = User.objects.get(email='ebk@ebk.com')
        szj = User.objects.get(email='szj@szj.com')
        hbb = User.objects.get(email='hbb@hbb.com')
        hgo = User.objects.get(email='hgo@hgo.com')
        dhl = User.objects.get(email='dhl@dhl.com')
        print('6명의 user들을 변수로 저장하여 불러왔습니다.')

        Token.objects.create(user=hjk)
        Token.objects.create(user=ebk)
        Token.objects.create(user=szj)
        Token.objects.create(user=hbb)
        Token.objects.create(user=hgo)
        Token.objects.create(user=dhl)
        print('6명의 user의 인증 토큰이 발급되었습니다.')

        # UserInfo.objects.create(user=hjk, nickname='권효진', birth='1995-02-11', tall=156)
        UserInfo.objects.create(user=hjk, nickname='권효진', birth='1995-02-11', region='서울', body_shape='보통체형',
                                personality=['유머있는', '차분한', '귀여운'], blood_type='AB형', smoking='비흡연',
                                introduce='안녕하세요 ^^')
        UserInfo.objects.create(user=ebk, nickname='권은비', birth='1991-04-03', tall=170)
        UserInfo.objects.create(user=szj, nickname='정수지', birth='1996-12-22', tall=158)
        UserInfo.objects.create(user=hbb, nickname='박홍빈', birth='1992-03-10', tall=170)
        UserInfo.objects.create(user=hgo, nickname='오형근', birth='1997-02-23', tall=173)
        UserInfo.objects.create(user=dhl, nickname='이도현', birth='1995-03-13', tall=184)
        print('UserInfo 테이블에 6명의 user 프로필정보가 생성되었습니다.')

        UserRibbon.objects.create(user=hjk, paid_ribbon=0, current_ribbon=50)
        UserRibbon.objects.create(user=ebk, paid_ribbon=0, current_ribbon=50)
        UserRibbon.objects.create(user=szj, paid_ribbon=0, current_ribbon=50)
        UserRibbon.objects.create(user=hbb, paid_ribbon=0, current_ribbon=50)
        UserRibbon.objects.create(user=hgo, paid_ribbon=0, current_ribbon=50)
        UserRibbon.objects.create(user=dhl, paid_ribbon=0, current_ribbon=50)
        print('계정을 생성한 6명의 user에게 기본 리본 50개가 지급되었습니다.')

        # 합격 여자
        Star.objects.create(user=man4, partner=hjk, star=5)
        Star.objects.create(user=man5, partner=hjk, star=2)
        Star.objects.create(user=man6, partner=hjk, star=4)
        # 심사중 여자
        Star.objects.create(user=man4, partner=szj, star=2)
        Star.objects.create(user=man5, partner=szj, star=3)
        # 합격 남자
        Star.objects.create(user=man1, partner=dhl, star=5)
        Star.objects.create(user=man2, partner=dhl, star=3)
        Star.objects.create(user=man3, partner=dhl, star=2)
        # 불합격 남자
        Star.objects.create(user=man1, partner=hbb, star=2)
        Star.objects.create(user=man2, partner=hbb, star=4)
        Star.objects.create(user=man3, partner=hbb, star=1)
        # 심사중 남자
        Star.objects.create(user=man2, partner=hgo, star=3)
        print('가입심사가 이루어졌습니다.')

        Story.objects.create(user=hjk, story=1, content='조용한 까페')
        Story.objects.create(user=hjk, story=3, content='네모네모 로직')
        print('스토리가 등록되었습니다.')

        UserIdealType.objects.create(user=hjk, tall_from=174, tall_to=180, age_from=25, age_to=35, region='서울', region2='경기')
        print('이상형정보가 등록되었습니다.')

        UserRibbon.objects.create(user=hjk, paid_ribbon=-5)
        print('리본 내역이 추가되었습니다.')


