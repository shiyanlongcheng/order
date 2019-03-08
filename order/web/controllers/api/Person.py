from web.controllers.api import route_api
from flask import request, jsonify
from common.libs.UrlManager import UrlManager
from common.libs.member.Checklogin import Checklogin

from common.models.order.commonweal.commonweal_order import CommonwealOrder
from common.models.order.take.takeout_order import TakeoutOrder
from common.models.order.second.second_order import SecondOrder
from common.models.order.express.express_order import ExpressOrder
from common.models.order.help.help_order import HelpOrder
from common.models.order.express.express_Image import ExpressImage
from sqlalchemy import or_


@route_api.route("/order/search", methods=["GET", "POST"])
def search():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    input = req['input'] if 'input' in req else ''
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not input or len(input) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    data_image = []
    if int(id) == 0:
        Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 0,
                                                             CommonwealOrder.commonweal_name.ilike(
                                                                 "%{0}%".format(req['input']))
                                                             )
        data_address = []
        if Commonweal_order_info is None:
            resp["data"] = data_address
            return jsonify(resp)
        if Commonweal_order_info:
            for item in Commonweal_order_info:
                express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 0,
                                                               ExpressImage.status == 1,
                                                               ExpressImage.eporder_id == item.id,
                                                               ExpressImage.eporder_sn == item.order_sn)
                if express_image_info:
                    for item1 in express_image_info:
                        tmp_image_data = UrlManager.buildCommonwealImageUrl(item1.imageurl)
                        data_image.append(tmp_image_data)
                tmp_data = {
                    'order_sn': item.order_sn,
                    'id': item.id,
                    'type_id': item.commonweal_type_id,
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
    elif int(id) == 1:
        Second_order_info = SecondOrder.query.filter(SecondOrder.status != 0,
                                                     SecondOrder.second_name.ilike(
                                                         "%{0}%".format(req['input']))
                                                     )
        data_address = []
        if Second_order_info is None:
            resp["data"] = data_address
            return jsonify(resp)
        if Second_order_info:
            for item in Second_order_info:
                express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 1,
                                                               ExpressImage.status == 1,
                                                               ExpressImage.eporder_id == item.id,
                                                               ExpressImage.eporder_sn == item.order_sn)
                if express_image_info:
                    for item1 in express_image_info:
                        tmp_image_data = UrlManager.buildSecondImageUrl(item1.imageurl)
                        data_image.append(tmp_image_data)
                tmp_data = {
                    'order_sn': item.order_sn,
                    'id': item.id,
                    'type_id': item.second_type_id,
                    'mid': item.order_member_id,
                    'rid': item.receipt_member_id,
                    'pay_price': item.pay_price,
                    'note': item.note,
                    'needplace': item.needplace,
                    'needtime': str(item.needtime),
                    'Second_title': item.second_name,
                    'Second_conment': item.second_conment,
                    'data_image': data_image,
                    'status': item.status
                }
                data_address.append(tmp_data)
        resp["data"] = data_address
        return jsonify(resp)
    elif int(id) == 2:
        Help_order_info = HelpOrder.query.filter(HelpOrder.status != 0,
                                                 HelpOrder.help_title.ilike(
                                                     "%{0}%".format(req['input']))
                                                 )
        data_address = []
        if Help_order_info is None:
            resp["data"] = data_address
            return jsonify(resp)
        if Help_order_info:
            for item in Help_order_info:
                express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 2,
                                                               ExpressImage.status == 1,
                                                               ExpressImage.eporder_id == item.id,
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
    elif int(id) == 3:
        Express_order_info = ExpressOrder.query.filter(ExpressOrder.status != 0,
                                                       or_(ExpressOrder.needplace.ilike(
                                                           "%{0}%".format(req['input'])),
                                                           ExpressOrder.express_place.ilike(
                                                               "%{0}%".format(req['input']))))
        data_address = []
        if Express_order_info is None:
            resp["data"] = data_address
            return jsonify(resp)
        if Express_order_info:
            for item in Express_order_info:
                express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 3,
                                                               ExpressImage.status == 1,
                                                               ExpressImage.eporder_id == item.id,
                                                               ExpressImage.eporder_sn == item.order_sn)
                if express_image_info:
                    for item1 in express_image_info:
                        tmp_image_data = UrlManager.buildImageUrl(item1.imageurl)
                        data_image.append(tmp_image_data)
                tmp_data = {
                    'order_sn': item.order_sn,
                    'sex': item.express_sex,
                    'id': item.id,
                    'pay_price': item.pay_price,
                    'note': item.note,
                    'mid': item.order_member_id,
                    'rid': item.receipt_member_id,
                    'needplace': item.needplace,
                    'Count': item.express_count,
                    'needtime': str(item.needtime),
                    'express_place': item.express_place,
                    'express_weight': item.express_weight,
                    'data_image': data_image,
                    'status': item.status
                }
                data_address.append(tmp_data)
        resp["data"] = data_address
        return jsonify(resp)
    elif int(id) == 4:
        Takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.status != 0,
                                                       or_(
                                                           TakeoutOrder.takeout_place.ilike(
                                                               "%{0}%".format(req['input'])),
                                                           TakeoutOrder.needplace.ilike(
                                                               "%{0}%".format(req['input']))
                                                       )
                                                       )
        data_address = []
        if Takeout_order_info is None:
            resp["data"] = data_address
            return jsonify(resp)
        if Takeout_order_info:
            for item in Takeout_order_info:
                Takeout_image_info = ExpressImage.query.filter(ExpressImage.type_id == 1,
                                                               ExpressImage.status == 1,
                                                               ExpressImage.eporder_id == item.id,
                                                               ExpressImage.eporder_sn == item.order_sn)
                if Takeout_image_info:
                    for item1 in Takeout_image_info:
                        tmp_image_data = UrlManager.buildImageUrl(item1.imageurl)
                        data_image.append(tmp_image_data)
                tmp_data = {
                    'order_sn': item.order_sn,
                    'sex': item.takeout_sex,
                    'id': item.id,
                    'pay_price': item.pay_price,
                    'note': item.note,
                    'mid': item.order_member_id,
                    'rid': item.receipt_member_id,
                    'needplace': item.needplace,
                    'Count': item.takeout_count,
                    'needtime': str(item.needtime),
                    'Takeout_place': item.takeout_place,
                    'Takeout_weight': item.takeout_weight,
                    'data_image': data_image,
                    'status': item.status
                }
                data_address.append(tmp_data)
        resp["data"] = data_address
        return jsonify(resp)


@route_api.route("/order/showPersonCommonweal", methods=["GET", "POST"])
def showPersonCommonweal():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    ip = req['ip'] if 'ip' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not ip or len(ip) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    data_image = []
    Commonweal_order_info = CommonwealOrder()
    if int(id) > -1:
        if int(ip) == 0:
            Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.status == 1,
                                                                 CommonwealOrder.order_member_id == member_info.id,
                                                                 CommonwealOrder.commonweal_type_id == id)
        elif int(ip) == 1:
            Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 1,
                                                                 CommonwealOrder.status != 0,
                                                                 CommonwealOrder.order_member_id == member_info.id,
                                                                 CommonwealOrder.commonweal_type_id == id)
    else:
        if int(ip) == 0:
            Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.status == 1,
                                                                 CommonwealOrder.order_member_id == member_info.id,
                                                                 )
        elif int(ip) == 1:
            Commonweal_order_info = CommonwealOrder.query.filter(CommonwealOrder.status != 1,
                                                                 CommonwealOrder.status != 0,
                                                                 CommonwealOrder.order_member_id == member_info.id,
                                                                 )

    data_address = []
    if Commonweal_order_info is None:
        resp["data"] = data_address
        return jsonify(resp)
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
                'type_id': item.commonweal_type_id,
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


@route_api.route("/order/showPersonSecond", methods=["GET", "POST"])
def showPersonSecond():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    ip = req['ip'] if 'ip' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not ip or len(ip) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    data_image = []
    Second_order_info = SecondOrder()
    if int(id) > -1:
        if int(ip) == 0:
            Second_order_info = SecondOrder.query.filter(SecondOrder.status == 1,
                                                         SecondOrder.order_member_id == member_info.id,
                                                         SecondOrder.second_type_id == id)
        elif int(ip) == 1:
            Second_order_info = SecondOrder.query.filter(SecondOrder.status != 1,
                                                         SecondOrder.status != 0,
                                                         SecondOrder.order_member_id == member_info.id,
                                                         SecondOrder.second_type_id == id)
    else:
        if int(ip) == 0:
            Second_order_info = SecondOrder.query.filter(SecondOrder.status == 1,
                                                         SecondOrder.order_member_id == member_info.id,
                                                         )
        elif int(ip) == 1:
            Second_order_info = SecondOrder.query.filter(SecondOrder.status != 1,
                                                         SecondOrder.status != 0,
                                                         SecondOrder.order_member_id == member_info.id,
                                                         )

    data_address = []
    if Second_order_info is None:
        resp["data"] = data_address
        return jsonify(resp)
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
                'id': item.id,
                'type_id': item.second_type_id,
                'mid': item.order_member_id,
                'rid': item.receipt_member_id,
                'pay_price': item.pay_price,
                'note': item.note,
                'needplace': item.needplace,
                'needtime': str(item.needtime),
                'Second_title': item.second_name,
                'Second_conment': item.second_conment,
                'data_image': data_image,
                'status': item.status
            }
            data_address.append(tmp_data)
    resp["data"] = data_address
    return jsonify(resp)


@route_api.route("/order/showPersonHelp", methods=["GET", "POST"])
def showPersonHelp():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    ip = req['ip'] if 'ip' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not ip or len(ip) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    data_image = []
    Help_order_info = HelpOrder()
    if int(id) == 0:
        if int(ip) == 0:
            Help_order_info = HelpOrder.query.filter(HelpOrder.order_member_id == member_info.id, )

        elif int(ip) > 0 and int(ip) < 5:
            Help_order_info = HelpOrder.query.filter(HelpOrder.status == ip,
                                                     HelpOrder.order_member_id == member_info.id,
                                                     )
        elif int(ip) == 5:
            Help_order_info = HelpOrder.query.filter(HelpOrder.status == 0,
                                                     HelpOrder.order_member_id == member_info.id,
                                                     )
        else:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
    elif int(id) == 1:
        if int(ip) == 0:
            Help_order_info = HelpOrder.query.filter(HelpOrder.receipt_member_id == member_info.id, )

        elif int(ip) > 0 and int(ip) < 5:
            Help_order_info = HelpOrder.query.filter(HelpOrder.status == int(ip) + 1,
                                                     HelpOrder.receipt_member_id == member_info.id,
                                                     )
        elif int(ip) == 5:
            Help_order_info = HelpOrder.query.filter(HelpOrder.status == 0,
                                                     HelpOrder.receipt_member_id == member_info.id,
                                                     )
        else:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
    else:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    data_address = []
    if Help_order_info is None:
        resp["data"] = data_address
        return jsonify(resp)
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


@route_api.route("/order/showPersonExpress", methods=["GET", "POST"])
def showPersonExpress():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    ip = req['ip'] if 'ip' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not ip or len(ip) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    data_image = []
    Express_order_info = ExpressOrder()
    if int(id) == 0:
        if int(ip) == 0:
            Express_order_info = ExpressOrder.query.filter(ExpressOrder.order_member_id == member_info.id, )

        elif int(ip) > 0 and int(ip) < 5:
            Express_order_info = ExpressOrder.query.filter(ExpressOrder.status == ip,
                                                           ExpressOrder.order_member_id == member_info.id,
                                                           )
        elif int(ip) == 5:
            Express_order_info = ExpressOrder.query.filter(ExpressOrder.status == 0,
                                                           ExpressOrder.order_member_id == member_info.id,
                                                           )
        else:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
    elif int(id) == 1:
        if int(ip) == 0:
            Express_order_info = ExpressOrder.query.filter(ExpressOrder.receipt_member_id == member_info.id, )

        elif int(ip) > 0 and int(ip) < 5:
            Express_order_info = ExpressOrder.query.filter(ExpressOrder.status == int(ip) + 1,
                                                           ExpressOrder.receipt_member_id == member_info.id,
                                                           )
        elif int(ip) == 5:
            Express_order_info = ExpressOrder.query.filter(ExpressOrder.status == 0,
                                                           ExpressOrder.receipt_member_id == member_info.id,
                                                           )
        else:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
    else:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    data_address = []
    if Express_order_info is None:
        resp["data"] = data_address
        return jsonify(resp)
    if Express_order_info:
        for item in Express_order_info:
            express_image_info = ExpressImage.query.filter(ExpressImage.type_id == 3,
                                                           ExpressImage.status == 1, ExpressImage.eporder_id == item.id,
                                                           ExpressImage.eporder_sn == item.order_sn)
            if express_image_info:
                for item1 in express_image_info:
                    tmp_image_data = UrlManager.buildImageUrl(item1.imageurl)
                    data_image.append(tmp_image_data)
            tmp_data = {
                'order_sn': item.order_sn,
                'sex': item.express_sex,
                'id': item.id,
                'pay_price': item.pay_price,
                'note': item.note,
                'mid': item.order_member_id,
                'rid': item.receipt_member_id,
                'needplace': item.needplace,
                'Count': item.express_count,
                'needtime': str(item.needtime),
                'express_place': item.express_place,
                'express_weight': item.express_weight,
                'data_image': data_image,
                'status': item.status
            }
            data_address.append(tmp_data)
    resp["data"] = data_address
    return jsonify(resp)


@route_api.route("/order/showPersonTakeout", methods=["GET", "POST"])
def showPersonTakeout():
    resp = {'code': 200, 'state': 'SUCCESS', 'url': '', 'title': '', 'original': '', 'msg': '', 'data': []}
    req = request.values
    id = req['id'] if 'id' in req else ''
    ip = req['ip'] if 'ip' in req else ''
    Codeq = request.headers.get('Authorization') if 'Authorization' in request.headers else ''
    if not Codeq or len(Codeq) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not id or len(id) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    if not ip or len(ip) < 1:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    member_info = Checklogin.check_login(Codeq)
    if member_info == False:
        resp["code"] = -1
        resp["msg"] = "你未注册"
        return jsonify(resp)
    data_image = []
    Takeout_order_info = TakeoutOrder()
    if int(id) == 0:
        if int(ip) == 0:
            Takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.order_member_id == member_info.id, )

        elif int(ip) > 0 and int(ip) < 5:
            Takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.status == ip,
                                                           TakeoutOrder.order_member_id == member_info.id,
                                                           )
        elif int(ip) == 5:
            Takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.status == 0,
                                                           TakeoutOrder.order_member_id == member_info.id,
                                                           )
        else:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
    elif int(id) == 1:
        if int(ip) == 0:
            Takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.receipt_member_id == member_info.id, )

        elif int(ip) > 0 and int(ip) < 5:
            Takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.status == int(ip) + 1,
                                                           TakeoutOrder.receipt_member_id == member_info.id,
                                                           )
        elif int(ip) == 5:
            Takeout_order_info = TakeoutOrder.query.filter(TakeoutOrder.status == 0,
                                                           TakeoutOrder.receipt_member_id == member_info.id,
                                                           )
        else:
            resp["code"] = -1
            resp["msg"] = "需要code"
            return jsonify(resp)
    else:
        resp["code"] = -1
        resp["msg"] = "需要code"
        return jsonify(resp)
    data_address = []
    if Takeout_order_info is None:
        resp["data"] = data_address
        return jsonify(resp)
    if Takeout_order_info:
        for item in Takeout_order_info:
            Takeout_image_info = ExpressImage.query.filter(ExpressImage.type_id == 1,
                                                           ExpressImage.status == 1, ExpressImage.eporder_id == item.id,
                                                           ExpressImage.eporder_sn == item.order_sn)
            if Takeout_image_info:
                for item1 in Takeout_image_info:
                    tmp_image_data = UrlManager.buildImageUrl(item1.imageurl)
                    data_image.append(tmp_image_data)
            tmp_data = {
                'order_sn': item.order_sn,
                'sex': item.takeout_sex,
                'id': item.id,
                'pay_price': item.pay_price,
                'note': item.note,
                'mid': item.order_member_id,
                'rid': item.receipt_member_id,
                'needplace': item.needplace,
                'Count': item.takeout_count,
                'needtime': str(item.needtime),
                'Takeout_place': item.takeout_place,
                'Takeout_weight': item.takeout_weight,
                'data_image': data_image,
                'status': item.status
            }
            data_address.append(tmp_data)
    resp["data"] = data_address
    return jsonify(resp)
