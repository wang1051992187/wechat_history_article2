import wechatsogou
from common import *
from bs4 import BeautifulSoup
import config
from Plug_in.showAPI_wechat import wechat_api
from Plug_in.rk import identify_image_callback_ruokuai_sogou, identify_image_callback_ruokuai_weixin
requests.packages.urllib3.disable_warnings()


class wechat_update(object):
    def __init__(self):
        self.now_time = int(time.time())
        self.wa = wechat_api()

    def temporary_to_perpetual(self, url):
        """
        将搜狗临时链接转化为永久链接
        :param url:
        :return:
        """
        url = url.replace("http:", "https:")
        return self.wa.get_permanent_url_other(url)

    def get_content(self, html):
        """
        根据HTML 获取正文内容
        :param html:
        :return:
        """
        try:
            soup = BeautifulSoup(html, 'lxml')
            content = soup.select('#js_content')[0].get_text().strip()
            content = content.replace(u'\xa0', u' ').replace(u'\u3000', u' ').replace("&quot;", "").replace("document.write(", "").replace("replace", "")
            return content
        except Exception:
            print_error(html)
            return None

    def get_all_banks(self):
        """
        获取所有银行列表
        :return:所有银行
        """
        file_obj = open(BANK_FILE, encoding='utf_8_sig')
        return file_obj.readlines()

    def wechat_info_list(self, nickname):
        """
        接入若快打码平台 获取公众号信息
        :param nickname: 公众号名称
        :return:
        """
        ocr_config = {
            'type': 'ruokuai',
            'dama_name': config.ruokuai_name,
            'dama_pswd': config.ruokuai_pswd,
            'dama_soft_id': config.ruokuai_soft_id,
            'dama_soft_key': config.ruokuai_soft_key
        }
        ws_api = wechatsogou.WechatSogouAPI(ocr_config=ocr_config)
        # 验证码输入错误的重试次数，默认为1
        ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)
        return ws_api.get_gzh_article_by_history(keyword=nickname, identify_image_callback_sogou=identify_image_callback_ruokuai_sogou, identify_image_callback_weixin=identify_image_callback_ruokuai_weixin)

    def out_of_date(self, get_time):
        """
        判断公众号文章时间是否已将超出需要爬取的时间段,超过返回True 停止爬取
        :param get_time:公众号文章时间
        :return:
        """
        return self.now_time - BEFORE_TIME > get_time

    def sogou_main(self):
        myConn_list = start_MySQL()
        cur = myConn_list[1]
        conn = myConn_list[0]

        for line in self.get_all_banks():
            try:
                nickname = line.replace("\n", "")
                print(nickname)
                wil = self.wechat_info_list(nickname)
                for article in wil['article']:
                    # 超过定时时间
                    if self.out_of_date(article['datetime']):
                        break
                    try:
                        article_info = self.temporary_to_perpetual(article['content_url'])
                        content = self.get_content(article_info['content'])
                        if content is not None:
                            data = {
                                # 微信公众号名称
                                'nickname': article_info['userName'],
                                # 公众号 LOGO
                                'userLogo': article_info['userLogo'],
                                # 公众号二维码
                                'userLogo_code': article_info['userLogo_code'],
                                # 内容图
                                'contentImg': article_info['contentImg'],
                                # 标题
                                'title': article['title'],
                                # 摘要
                                'digest': article['abstract'],
                                # 正文地址
                                'content_url': article_info['newUrl'],
                                # 时间
                                'datetime': article['datetime'],
                                'send_id': article['send_id'],
                                'fileid': article['fileid'],
                                'source_url': article['source_url'],
                                # 作者
                                'author': article['author'],
                                'copyright_stat': article['copyright_stat'],
                                # 正文
                                'content': content,
                            }
                            code = get_UUID(data['content_url'] + str(data['datetime']))
                            keywords = get_keywords(data['title'] + "," + data['digest'] + "," + data['content'])
                            keywords = sort_by_value(keywords)
                            summary = get_summary(RATE, data['content'])
                            sql = u'''INSERT INTO {}(nickname,title,digest,datetime,content_url,content,code,keywords,summary) VALUES ('{}', '{}', '{}', '{}', '{}','{}','{}',\"{}\",\"{}\")'''.format(MYSQL_TABLE_WECHAT_INFO, data['nickname'], data['title'], data['digest'], data['datetime'], data['content_url'], data['content'], code, keywords, summary.replace('"', '\\\"'))
                            print(sql)
                            sql2 = u'''INSERT INTO {}(nickname,title,digest,datetime,content_url,content,code,keywords,summary) VALUES ('{}', '{}', '{}', '{}', '{}','{}','{}',\"{}\",\"{}\")'''.format(MYSQL_TABLE_WECHAT_INFO_2, data['nickname'], data['title'], data['digest'], data['datetime'], data['content_url'], data['content'], code, keywords, summary.replace('"', '\\\"'))
                            # 保存到MYSQL
                            insert_mysql(cur, conn, sql)
                            # 是否备份数据库
                            if IS_BACK_UP:
                                insert_mysql(cur, conn, sql2)
                            # 保存到MongoDB
                            save_to_mongodb(data, nickname)
                            time.sleep(1)
                    except Exception as e:
                        print_error(e)
                        time.sleep(10)
            except AttributeError as e:
                print_error(e)
                time.sleep(10)
            time.sleep(5)
        close_MySQL(cur, conn)






