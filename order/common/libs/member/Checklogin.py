from common.libs.member.MemberService import MemberService
from common.models.member.member import Member


class Checklogin():
    @staticmethod
    def check_login(auth_cookie):
        if auth_cookie is None:
            return False
        auth_cookie = auth_cookie.split("#")
        if len(auth_cookie) != 2:
            return False
        try:
            member_info = Member.query.filter_by(id=auth_cookie[1]).first()
        except Exception:
            return False
        if member_info is None:
            return False
        if member_info.status == -1:
            return False
        if auth_cookie[0] != MemberService.geneAuthCode(member_info):
            return False
        return member_info
