from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from members.models import *

User = get_user_model()


class Command(BaseCommand):
    help = '깨끗한 상태의 DB에서 default로 유저 8명을 생성합니다.'

    def handle(self, *args, **kwargs):
        # User.objects.create_user(email='hjk@hjk.com', password='hjk', gender='여자')
        # User.objects.create_user(email='ebk@ebk.com', password='ebk', gender='여자')
        # User.objects.create_user(email='szj@szj.com', password='szj', gender='여자')
        # User.objects.create_user(email='mjk@mjk.com', password='mjk', gender='여자')
        # User.objects.create_user(email='hbb@hbb.com', password='hbb', gender='남자')
        # User.objects.create_user(email='hgo@hgo.com', password='hgo', gender='남자')
        # User.objects.create_user(email='dhl@dhl.com', password='dhl', gender='남자')
        # User.objects.create_user(email='jhm@jhm.com', password='jhm', gender='남자')
        # print('User 테이블에 8명의 user가 저장되었습니다.')

        hjk = User.objects.get(email='hjk@hjk.com')
        ebk = User.objects.get(email='ebk@ebk.com')
        szj = User.objects.get(email='szj@szj.com')
        mjk = User.objects.get(email='mjk@mjk.com')
        hbb = User.objects.get(email='hbb@hbb.com')
        hgo = User.objects.get(email='hgo@hgo.com')
        dhl = User.objects.get(email='dhl@dhl.com')
        jhm = User.objects.get(email='jhm@jhm.com')

        # UserInfo.objects.create(user=hjk, nickname='권효진', birth='1995-02-11', tall=156)
        # UserInfo.objects.create(user=ebk, nickname='권은비', birth='1991-04-03', tall=170)
        # UserInfo.objects.create(user=szj, nickname='정수지', birth='1996-12-22', tall=158)
        # UserInfo.objects.create(user=mjk, nickname='김민지', birth='1992-06-19', tall=150)
        # UserInfo.objects.create(user=hbb, nickname='박홍빈', birth='1992-03-10', tall=170)
        # UserInfo.objects.create(user=hgo, nickname='오형근', birth='1997-02-23', tall=173)
        # UserInfo.objects.create(user=dhl, nickname='이도현', birth='1995-03-13', tall=184)
        # UserInfo.objects.create(user=jhm, nickname='민지', birth='1995-07-17', tall=175)
        # print('UserInfo 테이블에 8명의 user 프로필정보가 저장되었습니다.')

        UserRibbon.objects.create(user=hjk, paid_ribbon=10, current_ribbon=10)
        UserRibbon.objects.create(user=ebk, paid_ribbon=10, current_ribbon=10)
        UserRibbon.objects.create(user=szj, paid_ribbon=10, current_ribbon=10)
        UserRibbon.objects.create(user=mjk, paid_ribbon=10, current_ribbon=10)
        UserRibbon.objects.create(user=hbb, paid_ribbon=10, current_ribbon=10)
        UserRibbon.objects.create(user=hgo, paid_ribbon=10, current_ribbon=10)
        UserRibbon.objects.create(user=dhl, paid_ribbon=10, current_ribbon=10)
        UserRibbon.objects.create(user=jhm, paid_ribbon=10, current_ribbon=10)
        print('계정을 생성한 8명의 user에게 기본 리본이 지급되었습니다.')

        # SendStar.objects.create(user=hgo, partner=hjk, star=5)
        # SendStar.objects.create(user=hbb, partner=hjk, star=3)
        # SendStar.objects.create(user=dhl, partner=hjk, star=4)
        # SendStar.objects.create(user=hjk, partner=hgo, star=5)
        # SendStar.objects.create(user=ebk, partner=hgo, star=3)
        # SendStar.objects.create(user=szj, partner=hgo, star=2)
        # SendStar.objects.create(user=jhm, partner=szj, star=2)
        # SendStar.objects.create(user=dhl, partner=szj, star=3)
        # print('8번의 가입심사가 이루어졌습니다.')


