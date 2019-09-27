import json
from Plug_in.ShowapiRequest import ShowapiRequest
import datetime
from config import *
from common import *

class wechat_api(object):
    def __init__(self):
        # API 调用次数
        self.call_count = 0
        # 错误次数
        self.error_count = 0

    def get_permanent_url_other(self, url):
        """
        调用付费接口进行查询
        :return:
        """
        self.call_count += 1
        print_error("当前已调用第{}次易源API接口".format(self.call_count))
        time_stamp = datetime.datetime.now()
        print("当前时间是：" + time_stamp.strftime('%Y.%m.%d %H:%M:%S'))
        print(url)
        showapi_appid = SHOWAPI_APPID
        showapi_config = SHOWAPI_SECRET
        r = ShowapiRequest("https://route.showapi.com/582-9", showapi_appid, showapi_config)
        r.addBodyPara("url", url)
        r.addBodyPara("needContent", "1")
        res = r.post()
        res = parse_page_index(str(res.text))
        if res['showapi_res_code'] != 0 or res['showapi_res_body']['ret_code'] != 0 or len(str(json.dumps(res['showapi_res_body']))) < 50:
            print_error("易源API错误")
            self.error_count += 1
            print("错误{}次".format(self.error_count))
            if self.error_count > 5:
                return None
            return self.get_permanent_url_other(url)
        else:
            return res['showapi_res_body']