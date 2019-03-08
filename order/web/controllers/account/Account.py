# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify

from common.models.log.AppAccesslog import AppAccessLog
from common.libs.Helper import iPagination, ops_render, getCurrentDate
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from application import app, db
from sqlalchemy import or_

route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = User.query

    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))
    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(User.uid).all()[offset:limit]
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("account/index.html", resp_data)


@route_account.route("/info")
def info():
    resp_data = {}
    req = request.values
    uid = int(req.get('id', 0))
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect(reback_url)
    info = User.query.filter_by(uid=uid).first()
    into=AppAccessLog.query.filter_by(uid=uid)
    if not info:
        return redirect(reback_url)
    if not into:
        info={}
    resp_data['into']=into[0:10]
    resp_data['info'] = info
    return ops_render("account/info.html", resp_data)


@route_account.route("/set", methods=["GET", "POST"])
def set():
    default_pwd = "******"
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get('id', 0))
        user_info = None
        if uid:
            user_info = User.query.filter_by(uid=uid).first()
        resp_data['info'] = user_info
        return ops_render("account/set.html", resp_data)
    resp = {
        'code': 200, 'msg': '操作成功', 'data': {}
    }
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    id1 = int(req['id']) if 'id' in req else 0
    mobile = req['mobile'] if 'mobile' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    email = req['email'] if 'email' in req else ''
    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~~~"
        return jsonify(resp)
    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~~~~"
        return jsonify(resp)
    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码~~~~"
        return jsonify(resp)
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录名~~~~"
        return jsonify(resp)
    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的密码~~~~"
        return jsonify(resp)
    has_in = User.query.filter(User.login_name == login_name, User.uid != id1).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "登陆名已经存在，请换一个试试吧~~~~~"
        return jsonify(resp)
    user_info = User.query.filter_by(uid=id1).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname
    model_user.email = email
    model_user.mobile = mobile
    model_user.login_name = login_name
    if login_pwd != default_pwd:
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.updated_time = getCurrentDate()
    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)


@route_account.route("/ops", methods=["POST"])
def ops():
    resp = {
        'code': 200, 'msg': '操作成功', 'data': {}
    }
    req = request.values
    id = int(req['id']) if 'id' in req else -1
    act = req['act'] if 'act' in req else ''
    if id is None or id < 0:
        resp['code'] = -1
        resp['msg'] = "请选择符合要操作的账号~~~~"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~~~"
        return jsonify(resp)
    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "不存在的账号~~~"
        return jsonify(resp)
    if act == 'remove':
        user_info.status = 0
    elif act == 'recover':
        user_info.status = 1
    app.logger.debug(user_info.status)
    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
