from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import time
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getCurrentDate
from common.libs.UploadService import UploadService
from common.libs.member.Checklogin import Checklogin
from common.models.order.express.address import MemberAddres
from common.models.order.second.second_order import SecondOrder
from common.models.order.express.express_Image import ExpressImage
from common.models.member.member import Member
from sqlalchemy import or_


@route_api.route("/order/sureSecond", methods=["GET", "POST"])
def sureSecond():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    express_order_info = SecondOrder.query.filter(SecondOrder.status != 0, SecondOrder.id == id,
                                                  SecondOrder.order_member_id == member_info.id).first()

    if express_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整1"
        return jsonify(resp)

    if express_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整2"
        return jsonify(resp)
    express_order_info.status = 4
    express_order_info.success_time = getCurrentDate()
    express_order_info.updated_time = getCurrentDate()
    db.session.add(express_order_info)
    db.session.commit()

    return jsonify(resp)


@route_api.route("/order/recSecond", methods=["GET", "POST"])
def recSecond():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    express_order_info = SecondOrder.query.filter(SecondOrder.status != 0, SecondOrder.id == id,
                                                  SecondOrder.receipt_member_id == member_info.id).first()
    if express_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    express_order_info.status = 3
    express_order_info.delivery_time = getCurrentDate()
    express_order_info.updated_time = getCurrentDate()
    db.session.add(express_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/deleteSecond", methods=["GET", "POST"])
def deleteSecond():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    express_order_info = SecondOrder.query.filter(SecondOrder.status != 0, SecondOrder.id == id,
                                                  SecondOrder.order_member_id == member_info.id).first()
    if express_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info.Balance = member_info.Balance + express_order_info.pay_price
    db.session.add(member_info)
    db.session.commit()
    express_order_info.status = 0
    express_order_info.updated_time = getCurrentDate()
    db.session.add(express_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/showPersonnalSecond", methods=["GET", "POST"])
def showPersonnalSecond():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    Second_order_info = SecondOrder.query.filter(SecondOrder.id == id,
                                                 or_(SecondOrder.receipt_member_id == member_info.id,
                                                     SecondOrder.order_member_id == member_info.id)).first()
    if Second_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    express_image_info = ExpressImage.query.filter(ExpressImage.status == 1,
                                                   ExpressImage.type_id == 1,
                                                   ExpressImage.eporder_id == Second_order_info.id,
                                                   ExpressImage.eporder_sn == Second_order_info.order_sn).all()
    if express_image_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)

    addres_info = MemberAddres.query.filter(MemberAddres.status == 1,
                                            MemberAddres.id == Second_order_info.needplaceid).first()
    if addres_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Rmember_info = Member.query.filter(Member.status != -1, Member.id == Second_order_info.receipt_member_id).first()
    if Rmember_info is None and Second_order_info.status != 1 and Second_order_info.status != 0:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    data_image = []
    if express_image_info:
        for item1 in express_image_info:
            tmp_image_data = UrlManager.buildSecondImageUrl(item1.imageurl)
            data_image.append(tmp_image_data)
    tmp_data = {
        'omem': {
            'name': addres_info.nickname,
            'weChatNum': addres_info.weChatNum,
            'oid': Second_order_info.order_member_id,
            'mobile': addres_info.mobile
        },
        'sex': Second_order_info.second_sex,
        'nid': Second_order_info.needplaceid,
        'detail': addres_info.hide_address,
        'order_sn': Second_order_info.order_sn,
        'id': Second_order_info.id,
        'mid': Second_order_info.order_member_id,
        'rid': Second_order_info.receipt_member_id,
        'pay_price': Second_order_info.pay_price,
        'original_price': Second_order_info.original_price,
        'note': Second_order_info.note,
        'needplace': Second_order_info.needplace,
        'needtime': str(Second_order_info.needtime),
        'Second_title': Second_order_info.second_name,
        'Second_conment': Second_order_info.second_conment,
        'data_image': data_image,
        'status': Second_order_info.status,
        'go_type_id': Second_order_info.second_go_type,
        'second_type_id': Second_order_info.second_type_id,
        'time': {
            'created_time': str(Second_order_info.created_time),
            'receipt_time': str(Second_order_info.receipt_time),
            'delivery_time': str(Second_order_info.delivery_time),
            'success_time': str(Second_order_info.success_time)
        }
    }
    if (Rmember_info):
        tmp_data['rmem'] = {
            'rid': Rmember_info.id,
            'name': Rmember_info.nickname,
            'weChatNum': Rmember_info.weChatNum,
            'mobile': Rmember_info.mobile
        }
    resp["data"] = tmp_data
    return jsonify(resp)


@route_api.route("/order/receiptSecond", methods=["GET", "POST"])
def receiptSecond():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    Second_order_info = SecondOrder.query.filter(SecondOrder.status != 0, SecondOrder.id == id).first()
    if Second_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Second_order_info.status = 2
    Second_order_info.receipt_member_id = member_info.id
    Second_order_info.receipt_time = getCurrentDate()
    Second_order_info.updated_time = getCurrentDate()
    db.session.add(Second_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/showSecond", methods=["GET", "POST"])
def showSecond():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    ip = req['ip'] if 'ip' in req else ''
    data_image = []
    if id and len(id) > 0:
        Second_order_info = SecondOrder.query.filter(SecondOrder.status != 0, SecondOrder.id == id).first()
        member_info = Member.query.filter(Member.status != -1, Member.id == Second_order_info.order_member_id).first()

        if Second_order_info is None:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        if member_info is None:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 1,
                                                       ExpressImage.status == 1,
                                                       ExpressImage.eporder_id == Second_order_info.id,
                                                       ExpressImage.eporder_sn == Second_order_info.order_sn)
        if express_image_info:
            for item1 in express_image_info:
                tmp_image_data = UrlManager.buildSecondImageUrl(item1.imageurl)
                data_image.append(tmp_image_data)
        tmp_data = {
            'nickname': member_info.nickname,
            'avatar': member_info.avatar,
            'mobile': member_info.mobile,
            'weChatNum': member_info.weChatNum,
            'order_sn': Second_order_info.order_sn,
            'id': Second_order_info.id,
            'pay_price': Second_order_info.pay_price,
            'note': Second_order_info.note,
            'second_go_type': Second_order_info.second_go_type,
            'needplace': Second_order_info.needplace,
            'needtime': str(Second_order_info.needtime),
            'second_title': Second_order_info.second_name,
            'second_conment': Second_order_info.second_conment,
            'status': Second_order_info.status,
            'data_image': data_image,
        }
        resp["data"] = tmp_data
        return jsonify(resp)
    Second_order_info = SecondOrder.query.filter(SecondOrder.status != 0)
    if ip and int(ip)-1 >-1:
        Second_order_info = SecondOrder.query.filter(SecondOrder.status != 0,
                                                     SecondOrder.second_type_id == (int(ip) - 1))
    data_address = []
    if Second_order_info:
        for item in Second_order_info:
            express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 1,
                                                           ExpressImage.status == 1, ExpressImage.eporder_id == item.id,
                                                           ExpressImage.eporder_sn == item.order_sn)
            if express_image_info:
                for item1 in express_image_info:
                    tmp_image_data = UrlManager.buildSecondImageUrl(item1.imageurl)
                    data_image.append(tmp_image_data)
            tmp_data = {
                'order_sn': item.order_sn,
                'sex': item.second_name,
                'id': item.id,
                'mid': item.order_member_id,
                'rid': item.receipt_member_id,
                'pay_price': item.pay_price,
                'note': item.note,
                'needplace': item.needplace,
                'needtime': str(item.needtime),
                'second_title': item.second_name,
                'second_conment': item.second_conment,
                'data_image': data_image,
                'status': item.status
            }
            data_address.append(tmp_data)
    resp["data"] = data_address
    return jsonify(resp)


@route_api.route("/order/addSecondOrder", methods=["GET", "POST"])
def addSecondOrder():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    default_address = req['default_address'] if 'default_address' in req else ''
    id = req['id'] if 'id' in req else ''
    conment = req['conment'] if 'conment' in req else ''
    default_addressid = req['default_addressid'] if 'default_addressid' in req else ''
    yun_price = req['yun_price'] if 'yun_price' in req else ''
    yuan_price = req['yuan_price'] if 'yuan_price' in req else ''
    go_type_id = req['go_type_id'] if 'go_type_id' in req else ''
    type_id = req['type_id'] if 'type_id' in req else ''
    title = req['title'] if 'title' in req else ''
    requirement = req['requirement'] if 'requirement' in req else ''
    sex = req['sex'] if 'sex' in req else None
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not go_type_id or len(go_type_id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not type_id or len(type_id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not default_address or len(default_address) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not default_addressid or len(default_addressid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整1"
        return jsonify(resp)
    if not yun_price or len(yun_price) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not yuan_price or len(yuan_price) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not conment or len(conment) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整2"
        return jsonify(resp)

    if not title or len(title) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整6"
        return jsonify(resp)
    if not sex or len(sex) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    Second_order_info = SecondOrder.query.filter(SecondOrder.order_member_id == member_info.id,
                                                 SecondOrder.id == id,
                                                 SecondOrder.status == 1).first()
    if id or len(id) > 1:
        if Second_order_info == None:
            resp["code"] = -1
            resp["msg"] = "信息不完整"
            return jsonify(resp)
    else:
        Second_order_info = SecondOrder()
        order_id = str(int(time.time() * 1000)) + str(int(time.clock() * 1000000))
        Second_order_info.order_member_id = member_info.id
        Second_order_info.order_sn = order_id
        Second_order_info.created_time = getCurrentDate()
        resp['data'] = order_id
    Second_order_info.pay_price = yun_price
    Second_order_info.original_price = yuan_price
    Second_order_info.needplace = default_address
    Second_order_info.needplaceid = default_addressid
    Second_order_info.needtime = getCurrentDate()
    Second_order_info.second_type_id = type_id
    Second_order_info.second_go_type = go_type_id
    Second_order_info.note = requirement
    Second_order_info.status = 1
    Second_order_info.second_name = title
    Second_order_info.second_conment = conment
    Second_order_info.second_sex = sex
    Second_order_info.updated_time = getCurrentDate()
    db.session.add(Second_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/deleteSecondImage", methods=["GET", "POST"])
def deleteSecondImage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    Second_orderid = req['Second_orderid'] if 'Second_orderid' in req else ''
    imagefile = req['imagefile'] if 'imagefile' in req else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not imagefile or len(imagefile) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    Second_order_info = SecondOrder.query.filter(SecondOrder.id == Second_orderid,
                                                 SecondOrder.order_member_id == member_info.id,
                                                 SecondOrder.status == 1).first()
    if Second_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整2"
        return jsonify(resp)
    if not Second_orderid or len(Second_orderid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整5"
        return jsonify(resp)
    app_config = app.config['APP']
    url = app_config['domain'] + app.config['UPLOAD']['order_second_url']
    image_info_in = ExpressImage.query.filter(ExpressImage.eporder_id == Second_order_info.id,
                                              ExpressImage.eporder_sn == Second_order_info.order_sn,
                                              ExpressImage.type_id == 1,
                                              ExpressImage.imageurl == imagefile.replace(url, ''),
                                              ExpressImage.status == 1).first()
    if image_info_in == None:
        resp["code"] = -1
        resp["msg"] = "信息不完整6"
        return jsonify(resp)
    if image_info_in:
        image_info_in.status = 0
        image_info_in.updated_time = getCurrentDate()
        db.session.add(image_info_in)
        db.session.commit()
    return jsonify(resp)


@route_api.route("/order/addSecondOrderImage", methods=["GET", "POST"])
def addSecondOrderImage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    file_target = request.files
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    Second_orderid = req['Second_orderid'] if 'Second_orderid' in req else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)

    if not Second_orderid or len(Second_orderid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    Second_order_info = SecondOrder.query.filter(SecondOrder.order_sn == Second_orderid,
                                                 SecondOrder.order_member_id == member_info.id,
                                                 SecondOrder.status == 1).first()
    if Second_order_info is None:
        resp["code"] = -1
        resp["msg"] = "上传失败"
        return jsonify(resp)
    config_upload = app.config['UPLOAD']
    if upfile:
        ret = UploadService.uploadImageFile(upfile, Second_orderid, config_upload['order_second_path'])
        if ret['code'] != '200':
            resp['state'] = '上传失败-1'
            resp['msg'] = ret['msg']
            return jsonify(resp)
        resp['url'] = ret['data']['file_key']

    image_info = ExpressImage()
    image_info.type_id = 1
    image_info.eporder_id = Second_order_info.id
    image_info.eporder_sn = Second_orderid
    image_info.imageurl = resp['url']
    image_info.updated_time = getCurrentDate()
    image_info.created_time = getCurrentDate()
    db.session.add(image_info)
    db.session.commit()
    return jsonify(resp)
