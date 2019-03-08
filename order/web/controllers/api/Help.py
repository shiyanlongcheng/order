from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import time
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getCurrentDate
from common.libs.UploadService import UploadService
from common.libs.member.Checklogin import Checklogin
from common.models.order.express.address import MemberAddres
from common.models.order.help.help_order import HelpOrder
from common.models.order.express.express_Image import ExpressImage
from common.models.member.member import Member
from sqlalchemy import or_


@route_api.route("/order/sureHelp", methods=["GET", "POST"])
def sureHelp():
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
    express_order_info = HelpOrder.query.filter(HelpOrder.status != 0, HelpOrder.id == id,
                                                HelpOrder.order_member_id == member_info.id).first()

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


@route_api.route("/order/recHelp", methods=["GET", "POST"])
def recHelp():
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
    express_order_info = HelpOrder.query.filter(HelpOrder.status != 0, HelpOrder.id == id,
                                                HelpOrder.receipt_member_id == member_info.id).first()
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


@route_api.route("/order/deleteHelp", methods=["GET", "POST"])
def deleteHelp():
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
    express_order_info = HelpOrder.query.filter(HelpOrder.status != 0, HelpOrder.id == id,
                                                HelpOrder.order_member_id == member_info.id).first()
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


@route_api.route("/order/showPersonnalHelp", methods=["GET", "POST"])
def showPersonnalHelp():
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
    Help_order_info = HelpOrder.query.filter(HelpOrder.id == id,
                                             or_(HelpOrder.receipt_member_id == member_info.id,
                                                 HelpOrder.order_member_id == member_info.id)).first()
    if Help_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    express_image_info = ExpressImage.query.filter(ExpressImage.status == 1,
                                                   ExpressImage.type_id == 2,
                                                   ExpressImage.eporder_id == Help_order_info.id,
                                                   ExpressImage.eporder_sn == Help_order_info.order_sn).all()
    if express_image_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)

    addres_info = MemberAddres.query.filter(MemberAddres.status == 1,
                                            MemberAddres.id == Help_order_info.needplaceid).first()
    if addres_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Rmember_info = Member.query.filter(Member.status != -1, Member.id == Help_order_info.receipt_member_id).first()
    if Rmember_info is None and Help_order_info.status != 1 and Help_order_info.status != 0:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    data_image = []
    if express_image_info:
        for item1 in express_image_info:
            tmp_image_data = UrlManager.buildHelpImageUrl(item1.imageurl)
            data_image.append(tmp_image_data)
    tmp_data = {
        'omem': {
            'name': addres_info.nickname,
            'weChatNum': addres_info.weChatNum,
            'oid': Help_order_info.order_member_id,
            'mobile': addres_info.mobile
        },
        'sex': Help_order_info.help_sex,
        'nid': Help_order_info.needplaceid,
        'detail': addres_info.hide_address,
        'order_sn': Help_order_info.order_sn,
        'id': Help_order_info.id,
        'mid': Help_order_info.order_member_id,
        'rid': Help_order_info.receipt_member_id,
        'pay_price': Help_order_info.pay_price,
        'note': Help_order_info.note,
        'needplace': Help_order_info.needplace,
        'needtime': str(Help_order_info.needtime),
        'Help_title': Help_order_info.help_title,
        'Help_conment': Help_order_info.help_conment,
        'data_image': data_image,
        'status': Help_order_info.status,
        'time': {
            'created_time': str(Help_order_info.created_time),
            'receipt_time': str(Help_order_info.receipt_time),
            'delivery_time': str(Help_order_info.delivery_time),
            'success_time': str(Help_order_info.success_time)
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


@route_api.route("/order/receiptHelp", methods=["GET", "POST"])
def receiptHelp():
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
    Help_order_info = HelpOrder.query.filter(HelpOrder.status != 0, HelpOrder.id == id).first()
    if Help_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    Help_order_info.status = 2
    Help_order_info.receipt_member_id = member_info.id
    Help_order_info.receipt_time = getCurrentDate()
    Help_order_info.updated_time = getCurrentDate()
    db.session.add(Help_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/showHelp", methods=["GET", "POST"])
def showHelp():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    data_image = []
    if id and len(id) > 0:
        Help_order_info = HelpOrder.query.filter(HelpOrder.status != 0, HelpOrder.id == id).first()
        member_info = Member.query.filter(Member.status != -1, Member.id == Help_order_info.order_member_id).first()

        if Help_order_info is None:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        if member_info is None:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 2,
                                                       ExpressImage.status == 1,
                                                       ExpressImage.eporder_id == Help_order_info.id,
                                                       ExpressImage.eporder_sn == Help_order_info.order_sn)
        if express_image_info:
            for item1 in express_image_info:
                tmp_image_data = UrlManager.buildHelpImageUrl(item1.imageurl)
                data_image.append(tmp_image_data)
        tmp_data = {
            'nickname': member_info.nickname,
            'avatar': member_info.avatar,
            'order_sn': Help_order_info.order_sn,
            'id': Help_order_info.id,
            'pay_price': Help_order_info.pay_price,
            'note': Help_order_info.note,
            'needplace': Help_order_info.needplace,
            'needtime': str(Help_order_info.needtime),
            'help_title': Help_order_info.help_title,
            'help_conment': Help_order_info.help_conment,
            'status': Help_order_info.status,
            'sex': Help_order_info.help_sex,
            'data_image': data_image,
        }
        resp["data"] = tmp_data
        return jsonify(resp)
    Help_order_info = HelpOrder.query.filter(HelpOrder.status != 0)
    data_address = []
    if Help_order_info:
        for item in Help_order_info:
            express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 2,
                                                           ExpressImage.status == 1, ExpressImage.eporder_id == item.id,
                                                           ExpressImage.eporder_sn == item.order_sn)
            if express_image_info:
                for item1 in express_image_info:
                    tmp_image_data = UrlManager.buildHelpImageUrl(item1.imageurl)
                    data_image.append(tmp_image_data)
            tmp_data = {
                'order_sn': item.order_sn,
                'sex': item.help_sex,
                'id': item.id,
                'mid': item.order_member_id,
                'rid': item.receipt_member_id,
                'pay_price': item.pay_price,
                'note': item.note,
                'needplace': item.needplace,
                'needtime': str(item.needtime),
                'help_title': item.help_title,
                'help_conment': item.help_conment,
                'data_image': data_image,
                'status': item.status
            }
            data_address.append(tmp_data)
    resp["data"] = data_address
    return jsonify(resp)


@route_api.route("/order/addHelpOrder", methods=["GET", "POST"])
def addHelpOrder():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    default_address = req['default_address'] if 'default_address' in req else ''
    id = req['id'] if 'id' in req else ''
    conment = req['conment'] if 'conment' in req else ''
    default_addressid = req['default_addressid'] if 'default_addressid' in req else ''
    data = req['data'] if 'data' in req else ''
    order_time = req['order_time'] if 'order_time' in req else ''
    yun_price = req['yun_price'] if 'yun_price' in req else ''
    expressCount = req['expressCount'] if 'expressCount' in req else ''
    title = req['title'] if 'title' in req else ''
    requirement = req['requirement'] if 'requirement' in req else ''
    sex = req['sex'] if 'sex' in req else None
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not default_address or len(default_address) < 1:
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
    if not conment or len(conment) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整2"
        return jsonify(resp)
    if not expressCount or len(expressCount) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整5"
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
    Help_order_info = HelpOrder.query.filter(HelpOrder.order_member_id == member_info.id,
                                             HelpOrder.id == id,
                                             HelpOrder.status == 1).first()
    if id or len(id) > 1:
        if Help_order_info == None:
            resp["code"] = -1
            resp["msg"] = "信息不完整"
            return jsonify(resp)
    else:
        if not yun_price or len(yun_price) < 1:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
        Help_order_info = HelpOrder()
        order_id = str(int(time.time() * 1000)) + str(int(time.clock() * 1000000))
        Help_order_info.order_member_id = member_info.id
        Help_order_info.order_sn = order_id
        Help_order_info.pay_price = yun_price
        Help_order_info.created_time = getCurrentDate()
        resp['data'] = order_id
    Help_order_info.needplace = default_address
    Help_order_info.needplaceid = default_addressid
    Help_order_info.needtime = data + " " + order_time
    Help_order_info.help_count = expressCount
    Help_order_info.note = requirement
    Help_order_info.status = 1
    Help_order_info.help_title = title
    Help_order_info.help_conment = conment
    Help_order_info.help_sex = sex
    Help_order_info.updated_time = getCurrentDate()
    db.session.add(Help_order_info)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/order/deleteHelpImage", methods=["GET", "POST"])
def deleteHelpImage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    Help_orderid = req['Help_orderid'] if 'Help_orderid' in req else ''
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
    Help_order_info = HelpOrder.query.filter(HelpOrder.id == Help_orderid,
                                             HelpOrder.order_member_id == member_info.id,
                                             HelpOrder.status == 1).first()
    if Help_order_info is None:
        resp["code"] = -1
        resp["msg"] = "信息不完整2"
        return jsonify(resp)
    if not Help_orderid or len(Help_orderid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整5"
        return jsonify(resp)
    app_config = app.config['APP']
    url = app_config['domain'] + app.config['UPLOAD']['order_help_url']
    image_info_in = ExpressImage.query.filter(ExpressImage.eporder_id == Help_order_info.id,
                                              ExpressImage.eporder_sn == Help_order_info.order_sn,
                                              ExpressImage.type_id == 2,
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


@route_api.route("/order/addHelpOrderImage", methods=["GET", "POST"])
def addHelpOrderImage():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    file_target = request.files
    req = request.values
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    Help_orderid = req['Help_orderid'] if 'Help_orderid' in req else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)

    if not Help_orderid or len(Help_orderid) < 1:
        resp["code"] = -1
        resp["msg"] = "信息不完整"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    Help_order_info = HelpOrder.query.filter(HelpOrder.order_sn == Help_orderid,
                                             HelpOrder.order_member_id == member_info.id,
                                             HelpOrder.status == 1).first()
    if Help_order_info is None:
        resp["code"] = -1
        resp["msg"] = "上传失败"
        return jsonify(resp)
    config_upload = app.config['UPLOAD']
    if upfile:
        ret = UploadService.uploadImageFile(upfile, Help_orderid, config_upload['order_Help_path'])
        if ret['code'] != '200':
            resp['state'] = '上传失败-1'
            resp['msg'] = ret['msg']
            return jsonify(resp)
        resp['url'] = ret['data']['file_key']

    image_info = ExpressImage()
    image_info.type_id = 2
    image_info.eporder_id = Help_order_info.id
    image_info.eporder_sn = Help_orderid
    image_info.imageurl = resp['url']
    image_info.updated_time = getCurrentDate()
    image_info.created_time = getCurrentDate()
    db.session.add(image_info)
    db.session.commit()
    return jsonify(resp)
