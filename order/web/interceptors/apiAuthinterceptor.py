from application import app
from flask import request, jsonify, g
from common.models.member.member import Member
from common.libs.member.MemberService import MemberService
from common.libs.UrlManager import UrlManager
import re
from common.libs.Logserver import LogService


@app.before_request
def before_request():
    ignore_urls = app.config['API_IGNORE_URLS']
    path = request.path
    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return
    if '/api' not in path:
        return
    member_info = check_login()

    g.current_user = None
    if member_info:
        g.member_info = member_info

    if not member_info:
        resp = {
            'code': -1, 'msg': '操作失败', 'data': {}
        }
        return jsonify(resp)
    return


# 判断登录
def check_login():
    auth_cookie = request.headers.get('Authorization')
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
    if member_info.status != 1:
        return False
    if auth_cookie[0] != MemberService.geneAuthCode(member_info):
        return False
    return member_info
