from web.controllers.api import route_api
from flask import request, jsonify, g
from application import app, db
import json
import requests
from common.models.member.member import Member
from common.models.member.oauth_member_bind import OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.UploadService import UploadService
from common.libs.member.MemberService import MemberService
from common.libs.member.Checklogin import Checklogin
from common.models.member.code import Code


@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {
        'code': 200, 'msg': '操作成功', 'data': {}
    }
    req = request.values
    code = req['code'] if 'code' in req else ''
    cod = req['cod'] if 'cod' in req else ''
    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else ''
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    app.logger.info(nickname)
    if not code or len(code) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
        app.config['APP_DATA']['appid'], app.config['APP_DATA']['appkey'], code)
    r = requests.get(url)
    res = json.loads(r.text)
    openid = res['openid']

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        if cod == '1':
            resp["code"] = -1
            resp["msg"] = "需要先去登陆"
            return jsonify(resp)
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.Balance = 0
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()
        bind_info = model_bind
    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    taken = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp["data"] = {'taken': taken, 'nickname': member_info.nickname, 'avatarUrl': member_info.avatar,
                    'balance': member_info.Balance, 'statu': member_info.status, 'name': member_info.name,
                    'mobile': member_info.mobile, 'weChatNum': member_info.weChatNum}
    return jsonify(resp)


@route_api.route("/member/uploadsMessage", methods=["GET", "POST"])
def uploadsMessage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': ''}
    file_target = request.files
    req = request.values
    comfirmCode = req['comfirmCode'] if 'comfirmCode' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    name = req['name'] if 'name' in req else ''
    weChatNum = req['weChatNum'] if 'weChatNum' in req else ''
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    app.logger.info(req)
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not comfirmCode or len(comfirmCode) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)

    if not mobile or len(mobile) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not name or len(name) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not weChatNum or len(weChatNum) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if upfile:
        ret = UploadService.uploadByFile(upfile)
        if ret['code'] != '200':
            resp['state'] = '上传失败-1'
            resp['msg'] = ret['msg']
            return jsonify(resp)
        resp['url'] = ret['data']['file_key']

    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "信息错误1"
        return jsonify(resp)
    code_info = Code.query.filter_by(mid=member_info.id).first()
    if code_info is None:
        resp["code"] = -1
        resp["msg"] = "信息错误"
        return jsonify(resp)
    if comfirmCode != code_info.code:
        resp["code"] = -1
        resp["msg"] = "信息错误2"
        return jsonify(resp)
    if member_info.status == 0:
        member_info.status = 1
    member_info.name = name
    member_info.mobile = mobile
    member_info.weChatNum = weChatNum
    member_info.schoolcode = resp['url']
    db.session.add(member_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/member/getMobile", methods=["GET", "POST"])
def getMobile():
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': ''}
    req = request.values
    mobile = req['mobile'] if 'mobile' in req else ''
    if mobile is None or len(mobile) < 11:
        resp['state'] = 'Fail'
        return jsonify(resp)
    token = req['token'] if 'token' in req else ''
    code = MemberService.get_code()
    member = Checklogin.check_login(token)
    if member is False:
        resp['state'] = 'Fail'
        return jsonify(resp)
    # url = 'http://utf8.api.smschinese.cn/?Uid={0}&Key={1}&smsMob={2}&smsText=验证码:{3}'.format(
    #     app.config['APP_DATA']['mobilename'], app.config['APP_DATA']['mobilekey'], mobile, code)
    # r = requests.post(url)
    # if r.text != '1':
    #     resp['state'] = 'Fail'
    #     return jsonify(resp)
    code_info = Code.query.filter_by(mid=member.id).first()
    if code_info is None:
        code_new = Code()
        code_new.creattime = getCurrentDate()
        code_new.mid = member.id
    else:
        code_new = code_info
    code_new.code = code
    code_new.updatetime = getCurrentDate()
    db.session.add(code_new)
    db.session.commit()
    return jsonify(resp)
