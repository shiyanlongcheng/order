SERVER_PORT = 1223
DEBUG = False
SQLALCHEMY_ECHO = False
JSON_AS_ASCII = False
AUTH_COOKIE_NAME = "app_school"
PAGE_SIZE = 10
PAGE_DISPLAY = 10
APP = {
    'domain': 'http://192.168.31.51:1223'
}
STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}
STATUS_MAPPING1 = {
    '0': "未认证用户",
    "1": "待认证",
    "-1": "黑名单",
    "100": "已认证"
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/member/',
    'order_express_path': '/web/static/upload/order/express/',
    'order_takeout_path': '/web/static/upload/order/takeout/',
    'order_Help_path': '/web/static/upload/order/help/',
    'order_second_path': '/web/static/upload/order/second/',
    'order_commonweal_path': '/web/static/upload/order/commonweal/',
    'member_url': '/static/upload/member',
    'order_express_url': '/static/upload/order/express/',
    'order_takeout_url': '/static/upload/order/takeout/',
    'order_help_url': '/static/upload/order/help/',
    'order_second_url': '/static/upload/order/second/',
    'order_commonweal_url': '/static/upload/order/commonweal/',
}
# 过路URL
IGNORE_URLS = [
    "^/user/login",
]
API_IGNORE_URLS = [
    "^/api/member/login"
]
IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "/favicon.ico"
]
APP_DATA = {
    'appid': 'wxab13618034248ef6',
    'appkey': '44eca2666e7db8d27f562a3aa1609083',
    'mobilekey': 'd41d8cd98f00b204e980',
    'mobilename': '诗言龙城'
}
