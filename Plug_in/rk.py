# -*- coding: utf-8 -*-
from hashlib import md5
import requests
from config import *
from common import *

class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.base_params = {
            'username': username,
            'password': md5(password.encode('utf-8')).hexdigest(),
            'softid': soft_id,
            'softkey': soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


def __identify_image_callback(img, code):
    try:
        username = ruokuai_name
        password = ruokuai_pswd
        id_ = ruokuai_soft_id
        key = ruokuai_soft_key
        rc = RClient(username, password, id_, key)
        result = rc.rk_create(img, code)
        print('验证码：', result['Result'])
        return result['Result']
    except Exception:
        raise Exception('识别验证码错误')


def identify_image_callback_ruokuai_sogou(img):
    print_error("开始识别验证码1")
    return __identify_image_callback(img, 3060)


def identify_image_callback_ruokuai_weixin(img):
    print_error("开始识别验证码2")
    return __identify_image_callback(img, 3040)