from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import time
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getCurrentDate
from common.libs.UploadService import UploadService
from common.libs.member.Checklogin import Checklogin
from common.models.order.express.address import MemberAddres
from common.models.order.take.takeout_order import TakeoutOrder
from common.models.order.express.express_Image import ExpressImage
from common.models.member.member import Member
from sqlalchemy import or_


@route_api.route("/order/sureTakeout", methods=["GET", "POST"])
def sureTakeout():
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
    express_order_info = TakeoutOrder.query.filter(TakeoutOrder.status != 0, TakeoutOrder.id == id,
                                                   TakeoutOrder.order_member_id == member_info.id).first()

    if express_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Rmember_info = Member.query.filter(Member.status == 100,
                                       Member.id == express_order_info.receipt_member_id).first()

    if express_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if Rmember_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Rmember_info.Balance = Rmember_info.Balance + express_order_info.pay_price
    express_order_info.status = 4
    express_order_info.success_time = getCurrentDate()
    express_order_info.updated_time = getCurrentDate()
    db.session.add(express_order_info)
    db.session.commit()
    db.session.add(Rmember_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/recTakeout", methods=["GET", "POST"])
def recTakeout():
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
    express_order_info = TakeoutOrder.query.filter(TakeoutOrder.status != 0, TakeoutOrder.id == id,
                                                   TakeoutOrder.receipt_member_id == member_info.id).first()
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


@route_api.route("/order/deleteTakeout", methods=["GET", "POST"])
def deleteTakeout():
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
    express_order_info = TakeoutOrder.query.filter(TakeoutOrder.status != 0, TakeoutOrder.id == id,
                                                   TakeoutOrder.order_member_id == member_info.id).first()
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


@route_api.route("/order/showPersonnalTakeout", methods=["GET", "POST"])
def showPersonnalTakeout():
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
    takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.id == id,
                                                   or_(TakeoutOrder.receipt_member_id == member_info.id,
                                                       TakeoutOrder.order_member_id == member_info.id)).first()
    if takeout_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    express_image_info = ExpressImage.query.filter(ExpressImage.status == 1,
                                                   ExpressImage.type_id == 4,
                                                   ExpressImage.eporder_id == takeout_order_info.id,
                                                   ExpressImage.eporder_sn == takeout_order_info.order_sn).all()
    if express_image_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)

    addres_info = MemberAddres.query.filter(MemberAddres.status == 1,
                                            MemberAddres.id == takeout_order_info.needplaceid).first()
    if addres_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Rmember_info = Member.query.filter(Member.status != -1, Member.id == takeout_order_info.receipt_member_id).first()
    if Rmember_info is None and takeout_order_info.status != 1 and takeout_order_info.status != 0:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    data_image = []
    if express_image_info:
        for item1 in express_image_info:
            tmp_image_data = UrlManager.buildTakeoutImageUrl(item1.imageurl)
            data_image.append(tmp_image_data)
    tmp_data = {
        'omem': {
            'name': addres_info.nickname,
            'weChatNum': addres_info.weChatNum,
            'oid': takeout_order_info.order_member_id,
            'mobile': addres_info.mobile
        },
        'sex': takeout_order_info.takeout_sex,
        'nid': takeout_order_info.needplaceid,
        'detail': addres_info.hide_address,
        'order_sn': takeout_order_info.order_sn,
        'id': takeout_order_info.id,
        'mid': takeout_order_info.order_member_id,
        'rid': takeout_order_info.receipt_member_id,
        'pay_price': takeout_order_info.pay_price,
        'note': takeout_order_info.note,
        'needplace': takeout_order_info.needplace,
        'Count': takeout_order_info.takeout_count,
        'needtime': str(takeout_order_info.needtime),
        'takeout_place': takeout_order_info.takeout_place,
        'takeout_weight': takeout_order_info.takeout_weight,
        'data_image': data_image,
        'name': takeout_order_info.takeout_name,
        'status': takeout_order_info.status,
        'weight_id': takeout_order_info.takeout_weight_id,
        'time': {
            'created_time': str(takeout_order_info.created_time),
            'receipt_time': str(takeout_order_info.receipt_time),
            'delivery_time': str(takeout_order_info.delivery_time),
            'success_time': str(takeout_order_info.success_time)
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


@route_api.route("/order/receiptTakeout", methods=["GET", "POST"])
def receiptTakeout():
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
    takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.status != 0, TakeoutOrder.id == id).first()
    if takeout_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    takeout_order_info.status = 2
    takeout_order_info.receipt_member_id = member_info.id
    takeout_order_info.receipt_time = getCurrentDate()
    takeout_order_info.updated_time = getCurrentDate()
    db.session.add(takeout_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/showTakeout", methods=["GET", "POST"])
def showTakeout():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    if id and len(id) > 0:
        takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.status != 0, TakeoutOrder.id == id).first()
        if takeout_order_info is None:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        tmp_data = {
            'order_sn': takeout_order_info.order_sn,
            'id': takeout_order_info.id,
            'pay_price': takeout_order_info.pay_price,
            'note': takeout_order_info.note,
            'needplace': takeout_order_info.needplace,
            'Count': takeout_order_info.takeout_count,
            'needtime': str(takeout_order_info.needtime),
            'takeout_place': takeout_order_info.takeout_place,
            'takeout_name': takeout_order_info.takeout_name,
            'takeout_weight': takeout_order_info.takeout_weight,
            'status': takeout_order_info.status,
            'sex': takeout_order_info.takeout_sex,
        }
        resp["data"] = tmp_data
        return jsonify(resp)
    takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.status != 0)
    data_address = []
    data_image = []
    if takeout_order_info:
        for item in takeout_order_info:
            express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 2,
                                                           ExpressImage.type_id == 4,
                                                           ExpressImage.status == 1, ExpressImage.eporder_id == item.id,
                                                           ExpressImage.eporder_sn == item.order_sn)
            if express_image_info:
                for item1 in express_image_info:
                    tmp_image_data = UrlManager.buildImageUrl(item1.imageurl)
                    data_image.append(tmp_image_data)
            tmp_data = {
                'order_sn': item.order_sn,
                'sex': item.takeout_sex,
                'id': item.id,
                'mid': item.order_member_id,
                'rid': item.receipt_member_id,
                'pay_price': item.pay_price,
                'note': item.note,
                'needplace': item.needplace,
                'Count': item.takeout_count,
                'needtime': str(item.needtime),
                'takeout_place': item.takeout_place,
                'takeout_weight': item.takeout_weight,
                'data_image': data_image,
                'status': item.status
            }
            data_address.append(tmp_data)
    resp["data"] = data_address
    return jsonify(resp)


@route_api.route("/order/addTakeoutOrder", methods=["GET", "POST"])
def addTakeoutOrder():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    default_address = req['default_address'] if 'default_address' in req else ''
    id = req['id'] if 'id' in req else ''
    takeout_name = req['takeout_name'] if 'takeout_name' in req else ''
    default_addressid = req['default_addressid'] if 'default_addressid' in req else ''
    data = req['data'] if 'data' in req else ''
    order_time = req['order_time'] if 'order_time' in req else ''
    yun_price = req['yun_price'] if 'yun_price' in req else ''
    expressCount = req['expressCount'] if 'expressCount' in req else ''
    takeoutplace = req['takeoutplace'] if 'takeoutplace' in req else ''
    weight_id = req['weight_id'] if 'weight_id' in req else ''
    requirement = req['requirement'] if 'requirement' in req else ''
    weight = req['weight'] if 'weight' in req else ''
    weight_id = req['weight_id'] if 'weight_id' in req else ''
    sex = req['sex'] if 'sex' in req else None
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not default_address or len(default_address) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not weight_id or len(weight_id) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    if not default_addressid or len(default_addressid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整1"
        return jsonify(resp)
    if not data or len(data) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整2"
        return jsonify(resp)
    if not order_time or len(order_time) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整3"
        return jsonify(resp)
    if not takeout_name or len(takeout_name) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整4"
        return jsonify(resp)
    if not expressCount or len(expressCount) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整5"
        return jsonify(resp)
    if not takeoutplace or len(takeoutplace) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整6"
        return jsonify(resp)
    if not weight or len(weight) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整7"
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
    takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.order_member_id == member_info.id,
                                                   TakeoutOrder.id == id,
                                                   TakeoutOrder.status == 1).first()
    if id or len(id) > 1:
        if takeout_order_info == None:
            resp["code"] = -1
            resp["msg"] = "信息不完整"
            return jsonify(resp)
    else:
        if not yun_price or len(yun_price) < 1:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        takeout_order_info = TakeoutOrder()
        order_id = str(int(time.time() * 1000)) + str(int(time.clock() * 1000000))
        takeout_order_info.order_member_id = member_info.id
        takeout_order_info.order_sn = order_id
        takeout_order_info.pay_price = yun_price
        takeout_order_info.created_time = getCurrentDate()
        resp['data'] = order_id
    takeout_order_info.needplace = default_address
    takeout_order_info.needplaceid = default_addressid
    takeout_order_info.needtime = data + " " + order_time
    takeout_order_info.takeout_count = expressCount
    takeout_order_info.note = requirement
    takeout_order_info.status = 1
    takeout_order_info.takeout_place = takeoutplace
    takeout_order_info.takeout_name = takeout_name
    takeout_order_info.takeout_weight = weight
    takeout_order_info.takeout_weight_id = weight_id
    takeout_order_info.takeout_sex = sex
    takeout_order_info.updated_time = getCurrentDate()
    db.session.add(takeout_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/deleteTakeoutImage", methods=["GET", "POST"])
def deleteTakeoutImage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    takeout_orderid = req['takeout_orderid'] if 'takeout_orderid' in req else ''
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
    takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.id == takeout_orderid,
                                                   TakeoutOrder.order_member_id == member_info.id,
                                                   TakeoutOrder.status == 1).first()
    if takeout_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整4"
        return jsonify(resp)
    if not takeout_orderid or len(takeout_orderid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整5"
        return jsonify(resp)
    app_config = app.config['APP']
    url = app_config['domain'] + app.config['UPLOAD']['order_takeout_url']
    image_info_in = ExpressImage.query.filter(ExpressImage.eporder_id == takeout_order_info.id,
                                              ExpressImage.eporder_sn == takeout_order_info.order_sn,
                                              ExpressImage.type_id == 4,
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


@route_api.route("/order/addTakeoutOrderImage", methods=["GET", "POST"])
def addTakeoutOrderImage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    file_target = request.files
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    takeout_orderid = req['takeout_orderid'] if 'takeout_orderid' in req else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)

    if not takeout_orderid or len(takeout_orderid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.order_sn == takeout_orderid,
                                                   TakeoutOrder.order_member_id == member_info.id,
                                                   TakeoutOrder.status == 1).first()
    if takeout_order_info is None:
        resp["code"] = -1
        resp["msg"] = "上传失败"
        return jsonify(resp)
    config_upload = app.config['UPLOAD']
    if upfile:
        ret = UploadService.uploadImageFile(upfile, takeout_orderid, config_upload['order_takeout_path'])
        if ret['code'] != '200':
            resp['state'] = '上传失败-1'
            resp['msg'] = ret['msg']
            return jsonify(resp)
        resp['url'] = ret['data']['file_key']

    image_info = ExpressImage()
    image_info.type_id = 4
    image_info.eporder_id = takeout_order_info.id
    image_info.eporder_sn = takeout_orderid
    image_info.imageurl = resp['url']
    image_info.updated_time = getCurrentDate()
    image_info.created_time = getCurrentDate()
    db.session.add(image_info)
    db.session.commit()
    return jsonify(resp)
