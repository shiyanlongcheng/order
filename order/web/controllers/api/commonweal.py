from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import time
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getCurrentDate
from common.libs.UploadService import UploadService
from common.libs.member.Checklogin import Checklogin
from common.models.order.express.address import MemberAddres
from common.models.order.commonweal.commonweal_order import CommonwealOrder
from common.models.order.express.express_Image import ExpressImage
from common.models.member.member import Member
from sqlalchemy import or_


@route_api.route("/order/sureCommonweal", methods=["GET", "POST"])
def sureCommonweal():
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
    express_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 0, CommonwealOrder.id == id,
                                                      CommonwealOrder.order_member_id == member_info.id).first()

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


@route_api.route("/order/recCommonweal", methods=["GET", "POST"])
def recCommonweal():
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
    express_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 0, CommonwealOrder.id == id,
                                                      CommonwealOrder.receipt_member_id == member_info.id).first()
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


@route_api.route("/order/deleteCommonweal", methods=["GET", "POST"])
def deleteCommonweal():
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
    express_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 0, CommonwealOrder.id == id,
                                                      CommonwealOrder.order_member_id == member_info.id).first()
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


@route_api.route("/order/showPersonnalCommonweal", methods=["GET", "POST"])
def showPersonnalCommonweal():
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
    Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.id == id,
                                                         or_(CommonwealOrder.receipt_member_id == member_info.id,
                                                             CommonwealOrder.order_member_id == member_info.id)).first()
    if Commonweal_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    express_image_info = ExpressImage.query.filter(ExpressImage.status == 1,
                                                   ExpressImage.type_id == 0,
                                                   ExpressImage.eporder_id == Commonweal_order_info.id,
                                                   ExpressImage.eporder_sn == Commonweal_order_info.order_sn).all()
    if express_image_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)

    addres_info = MemberAddres.query.filter(MemberAddres.status == 1,
                                            MemberAddres.id == Commonweal_order_info.needplaceid).first()
    if addres_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Rmember_info = Member.query.filter(Member.status != -1,
                                       Member.id == Commonweal_order_info.receipt_member_id).first()
    if Rmember_info is None and Commonweal_order_info.status != 1 and Commonweal_order_info.status != 0:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    data_image = []
    if express_image_info:
        for item1 in express_image_info:
            tmp_image_data = UrlManager.buildCommonwealImageUrl(item1.imageurl)
            data_image.append(tmp_image_data)
    tmp_data = {
        'omem': {
            'name': addres_info.nickname,
            'weChatNum': addres_info.weChatNum,
            'oid': Commonweal_order_info.order_member_id,
            'mobile': addres_info.mobile
        },
        'nid': Commonweal_order_info.needplaceid,
        'detail': addres_info.hide_address,
        'order_sn': Commonweal_order_info.order_sn,
        'id': Commonweal_order_info.id,
        'mid': Commonweal_order_info.order_member_id,
        'rid': Commonweal_order_info.receipt_member_id,
        'type_id': Commonweal_order_info.commonweal_type_id,
        'pay_price': Commonweal_order_info.pay_price,
        'note': Commonweal_order_info.note,
        'needplace': Commonweal_order_info.needplace,
        'needtime': str(Commonweal_order_info.needtime),
        'Commonweal_title': Commonweal_order_info.commonweal_name,
        'Commonweal_conment': Commonweal_order_info.commonweal_conment,
        'data_image': data_image,
        'status': Commonweal_order_info.status,
        'time': {
            'created_time': str(Commonweal_order_info.created_time),
            'receipt_time': str(Commonweal_order_info.receipt_time),
            'delivery_time': str(Commonweal_order_info.delivery_time),
            'success_time': str(Commonweal_order_info.success_time)
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


@route_api.route("/order/receiptCommonweal", methods=["GET", "POST"])
def receiptCommonweal():
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
    Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 0, CommonwealOrder.id == id).first()
    if Commonweal_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Commonweal_order_info.status = 2
    Commonweal_order_info.receipt_member_id = member_info.id
    Commonweal_order_info.receipt_time = getCurrentDate()
    Commonweal_order_info.updated_time = getCurrentDate()
    db.session.add(Commonweal_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/showCommonweal", methods=["GET", "POST"])
def showCommonweal():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    data_image = []
    if id and len(id) > 0:
        Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 0,
                                                             CommonwealOrder.id == id).first()
        member_info = Member.query.filter(Member.status != -1,
                                          Member.id == Commonweal_order_info.order_member_id).first()

        if Commonweal_order_info is None:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        if member_info is None:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 0,
                                                       ExpressImage.status == 1,
                                                       ExpressImage.eporder_id == Commonweal_order_info.id,
                                                       ExpressImage.eporder_sn == Commonweal_order_info.order_sn)
        if express_image_info:
            for item1 in express_image_info:
                tmp_image_data = UrlManager.buildCommonwealImageUrl(item1.imageurl)
                data_image.append(tmp_image_data)
        tmp_data = {
            'nickname': member_info.nickname,
            'avatar': member_info.avatar,
            'mobile': member_info.mobile,
            'type_id': Commonweal_order_info.commonweal_type_id,
            'weChatNum': member_info.weChatNum,
            'order_sn': Commonweal_order_info.order_sn,
            'id': Commonweal_order_info.id,
            'note': Commonweal_order_info.note,
            'needplace': Commonweal_order_info.needplace,
            'needtime': str(Commonweal_order_info.needtime),
            'Commonweal_title': Commonweal_order_info.commonweal_name,
            'Commonweal_conment': Commonweal_order_info.commonweal_conment,
            'status': Commonweal_order_info.status,
            'data_image': data_image,
        }
        resp["data"] = tmp_data
        return jsonify(resp)
    Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 0)
    data_address = []
    if Commonweal_order_info:
        for item in Commonweal_order_info:
            express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 0,
                                                           ExpressImage.status == 1, ExpressImage.eporder_id == item.id,
                                                           ExpressImage.eporder_sn == item.order_sn)
            if express_image_info:
                for item1 in express_image_info:
                    tmp_image_data = UrlManager.buildCommonwealImageUrl(item1.imageurl)
                    data_image.append(tmp_image_data)
            tmp_data = {
                'order_sn': item.order_sn,
                'id': item.id,
                'type_id':item.commonweal_type_id,
                'mid': item.order_member_id,
                'rid': item.receipt_member_id,
                'pay_price': item.pay_price,
                'note': item.note,
                'needplace': item.needplace,
                'needtime': str(item.needtime),
                'Commonweal_title': item.commonweal_name,
                'Commonweal_conment': item.commonweal_conment,
                'data_image': data_image,
                'status': item.status
            }
            data_address.append(tmp_data)
    resp["data"] = data_address
    return jsonify(resp)


@route_api.route("/order/addCommonwealOrder", methods=["GET", "POST"])
def addCommonwealOrder():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    default_address = req['default_address'] if 'default_address' in req else ''
    id = req['id'] if 'id' in req else ''
    conment = req['conment'] if 'conment' in req else ''
    default_addressid = req['default_addressid'] if 'default_addressid' in req else ''
    title = req['title'] if 'title' in req else ''
    requirement = req['requirement'] if 'requirement' in req else ''
    type_id = req['type_id'] if 'type_id' in req else ''
    sex = req['sex'] if 'sex' in req else None
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not type_id or len(type_id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整1"
        return jsonify(resp)
    if not default_address or len(default_address) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整2"
        return jsonify(resp)
    if not default_addressid or len(default_addressid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整1"
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
        resp["msg"] = "信息不完整5"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.order_member_id == member_info.id,
                                                         CommonwealOrder.id == id,
                                                         CommonwealOrder.status == 1).first()
    if id or len(id) > 1:
        if Commonweal_order_info == None:
            resp["code"] = -1
            resp["msg"] = "信息不完整"
            return jsonify(resp)
    else:
        Commonweal_order_info = CommonwealOrder()
        order_id = str(int(time.time() * 1000)) + str(int(time.clock() * 1000000))
        Commonweal_order_info.order_member_id = member_info.id
        Commonweal_order_info.order_sn = order_id
        Commonweal_order_info.created_time = getCurrentDate()
        resp['data'] = order_id
    Commonweal_order_info.pay_price = 0
    Commonweal_order_info.needplace = default_address
    Commonweal_order_info.needplaceid = default_addressid
    Commonweal_order_info.needtime = getCurrentDate()
    Commonweal_order_info.commonweal_type_id = type_id
    Commonweal_order_info.note = requirement
    Commonweal_order_info.status = 1
    Commonweal_order_info.commonweal_name = title
    Commonweal_order_info.commonweal_conment = conment
    Commonweal_order_info.commonweal_sex = sex
    Commonweal_order_info.updated_time = getCurrentDate()
    db.session.add(Commonweal_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/deleteCommonwealImage", methods=["GET", "POST"])
def deleteCommonwealImage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    Commonweal_orderid = req['Commonweal_orderid'] if 'Commonweal_orderid' in req else ''
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
    Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.id == Commonweal_orderid,
                                                         CommonwealOrder.order_member_id == member_info.id,
                                                         CommonwealOrder.status == 1).first()
    if Commonweal_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整2"
        return jsonify(resp)
    if not Commonweal_orderid or len(Commonweal_orderid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整5"
        return jsonify(resp)
    app_config = app.config['APP']
    url = app_config['domain'] + app.config['UPLOAD']['order_commonweal_url']
    image_info_in = ExpressImage.query.filter(ExpressImage.eporder_id == Commonweal_order_info.id,
                                              ExpressImage.eporder_sn == Commonweal_order_info.order_sn,
                                              ExpressImage.type_id == 0,
                                              ExpressImage.imageurl == imagefile.replace(url, ''),
                                              ExpressImage.status == 1
                                              ).first()
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


@route_api.route("/order/addCommonwealOrderImage", methods=["GET", "POST"])
def addCommonwealOrderImage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    file_target = request.files
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    Commonweal_orderid = req['Commonweal_orderid'] if 'Commonweal_orderid' in req else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)

    if not Commonweal_orderid or len(Commonweal_orderid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.order_sn == Commonweal_orderid,
                                                         CommonwealOrder.order_member_id == member_info.id,
                                                         CommonwealOrder.status == 1).first()
    if Commonweal_order_info is None:
        resp["code"] = -1
        resp["msg"] = "上传失败"
        return jsonify(resp)
    config_upload = app.config['UPLOAD']
    if upfile:
        ret = UploadService.uploadImageFile(upfile, Commonweal_orderid, config_upload['order_commonweal_path'])
        if ret['code'] != '200':
            resp['state'] = '上传失败-1'
            resp['msg'] = ret['msg']
            return jsonify(resp)
        resp['url'] = ret['data']['file_key']

    image_info = ExpressImage()
    image_info.type_id = 0
    image_info.eporder_id = Commonweal_order_info.id
    image_info.eporder_sn = Commonweal_orderid
    image_info.imageurl = resp['url']
    image_info.updated_time = getCurrentDate()
    image_info.created_time = getCurrentDate()
    db.session.add(image_info)
    db.session.commit()
    return jsonify(resp)
