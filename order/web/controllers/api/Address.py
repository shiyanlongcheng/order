from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db

from common.libs.Helper import getCurrentDate
from common.libs.member.Checklogin import Checklogin
from common.models.order.express.address import MemberAddres
from common.models.order.type import Type
from common.models.order.express.expressAddress import ExpressAddres


@route_api.route("/order/deleteAddress", methods=["GET", "POST"])
def deleteAddress():
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    ID = request.values.get('id') if 'id' in request.values else ''
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    address_info = MemberAddres.query.filter(MemberAddres.member_id == member_info.id, MemberAddres.id == ID,
                                             MemberAddres.status == 1).first()
    if address_info is None:
        resp["code"] = -1
        resp["msg"] = "信息错误"
        return jsonify(resp)
    address_info.status = 0
    address_info.updated_time = getCurrentDate()
    db.session.add(address_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/showType", methods=["GET", "POST"])
def showtype():
    resp = {'code':200,'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    type1_info = Type.query.filter(Type.lagetypeid == 1, Type.status == 1)
    type2_info = Type.query.filter(Type.lagetypeid == 2, Type.status == 1)
    if type1_info is None:
        resp["code"] = -1
        resp["msg"] = "信息错误"
        return jsonify(resp)
    if type2_info is None:
        resp["code"] = -1
        resp["msg"] = "信息错误"
        return jsonify(resp)
    data_address = []
    data_expressAddres = []
    if type1_info:
        for item in type1_info:
            tmp_data = item.type_title
            data_address.append(tmp_data)
    if type2_info:
        for item in type2_info:
            tmp_data = item.type_title,
            data_expressAddres.append(tmp_data)
    resp["type_1"] = data_address
    resp["type_2"] = data_expressAddres
    return jsonify(resp)


@route_api.route("/order/showDefaultAddress", methods=["GET", "POST"])
def showAddress():
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    address_info = MemberAddres.query.filter(MemberAddres.member_id == member_info.id, MemberAddres.status == 1)
    expressAddres_info = ExpressAddres.query.filter(ExpressAddres.status == 1)
    if address_info is None:
        resp["code"] = -1
        resp["msg"] = "信息错误"
        return jsonify(resp)
    if expressAddres_info is None:
        resp["code"] = -1
        resp["msg"] = "信息错误"
        return jsonify(resp)
    data_address = []
    data_expressAddres = []
    if address_info:
        for item in address_info:
            tmp_data = {
                'nickname': item.nickname,
                'id': item.id,
                'mobile': item.mobile,
                'weChatNum': item.weChatNum,
                'region': [item.province_str, item.city_str, item.area_str],
                'address': item.address,
                'hide_address': item.hide_address,
                'detail': item.city_str + item.area_str + item.address
            }
            data_address.append(tmp_data)
    if expressAddres_info:
        for item in expressAddres_info:
            tmp_data = item.expressAddress,
            data_expressAddres.append(tmp_data)
    resp["data"] = data_address
    resp["expressAddres"] = data_expressAddres
    return jsonify(resp)


@route_api.route("/order/address", methods=["GET", "POST"])
def address():
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': ''}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    id = req['id'] if 'id' in req else ''
    address = req['address'] if 'address' in req else ''
    weChatNum = req['weChatNum'] if 'weChatNum' in req else ''
    region = req['region'] if 'region' in req else None
    region_info = region.split(',')

    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not nickname or len(nickname) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)

    if not mobile or len(mobile) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not region_info or len(region_info) != 3:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not address or len(address) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)

    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "信息错误1"
        return jsonify(resp)
    if id and len(id) > 0 and int(id) > -1:
        address_info = MemberAddres.query.filter_by(id=id).first()
        if address_info is None:
            resp["code"] = -1
            resp["msg"] = "信息错误"
            return jsonify(resp)
        if address_info.member_id != member_info.id:
            resp["code"] = -1
            resp["msg"] = "信息错误"
            return jsonify(resp)
    elif id and int(id) == -1:
        address_info = MemberAddres()
        address_info.created_time = getCurrentDate()
    else:
        resp["code"] = -1
        resp["msg"] = "信息错误"
        return jsonify(resp)
    app.logger.info(region_info[1])
    address_info.member_id = member_info.id
    address_info.nickname = nickname
    address_info.mobile = mobile
    address_info.weChatNum = weChatNum
    address_info.province_str = region_info[0]
    address_info.city_str = region_info[1]
    address_info.area_str = region_info[2]
    address_info.status = 1
    address_info.address = address
    address_info.updated_time = getCurrentDate()
    db.session.add(address_info)
    db.session.commit()
    return jsonify(resp)
