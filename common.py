import requests
import csv
import json
from json.decoder import JSONDecodeError
import time
import pymongo
from config import *
import sys
import hashlib
import pymysql
import uuid
import random
import jieba.analyse

cookie = "pt2gguin=o1051992187; RK=IEixJVhVaw; ptcz=be8e77ec912637844e9c1428b7c0730abbcd2cf720b1d7e3be3a4d9bf3a1edbd; pgv_pvid=9880978732; o_cookie=1051992187; pac_uid=1_1051992187; pgv_pvi=3591453696; ptui_loginuin=2833184355; ua_id=GBifREM49IoudmkWAAAAAPiKVkwrVsdNekvo16Gcy8A=; __lnkrntdmcvrd=-1; noticeLoginFlag=1; ts_uid=1573555124; remember_acct=1051992187%40qq.com; mm_lang=zh_CN; xid=48b9653d884f265431f9e77e811edd15; openid2ticket_opoTWstNaY2vSCe77gcxGZUnGV1s=28coiKmqn2AnXdm22ZaXeNEXRZmrWZHHIe1myIF/8Ug=; rewardsn=; wxtokenkey=777"
header = {
    "Cookie": cookie,
    "Host": "mp.weixin.qq.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Connection": "close",
    "If-Modified-Since": "Fri, 27 Jul 2018 09:24:20 +0800",
    "Accept-Encoding": 'gzip, deflate, br',
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    "Cache-Control": 'max-age=0'
}

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_page_detail(url):
    """
    返回请求的html
    :param url:
    :return:
    """
    try:
        response = requests.get(url, headers=header, verify=False)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print_error('Error occurred')
        return None


def requests_post(url, data):
    """
    post 请求
    :param url:
    :param data:
    :return:
    """
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError as e:
        print(e)
        print('Error occurred')
        return None


def sort_by_value(data):
    """
    dict 数据按 value 倒序排序
    :param data:
    :return:
    """
    cnt = 0
    dic = {}
    after = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    for key, value in after.items():
        cnt += 1
        if cnt > TOP_NUM:
            break
        dic[key] = value
    return dic


def get_keywords(doc):
    """
    获取关键词
    :param doc:
    :return:
    """
    di = {}
    tags_1 = jieba.analyse.extract_tags(doc, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v','a','eng','nr','nt','nz','vd','vn'))
    for f in tags_1:
        di[f[0]] = f[1]
    return di


def get_summary(rate, doc):
    """
    获取摘要内容
    :param rate:
    :param doc:
    :return:
    """
    try:
        data = {
            'length_rate': rate,
            'doc': doc
        }
        html = requests_post(SUMMARY_URL, json.dumps(data))
        data_json = json.loads(html)
        return data_json['result']['result']
    except Exception as e:
        print(e)
        return doc


def save_to_csv(data_res, titles, path='D://data.csv'):
    """
    保存csv格式
    :param data_res: 保存的数据
    :param titles: 标题
    :param path: 位置
    :return:
    """
    with open(path, 'w', encoding='utf_8_sig', newline='') as file:
        wrote = csv.writer(file)
        wrote.writerow(titles)
        wrote.writerows(data_res)


def start_MySQL():
    """
    MYSQL数据库操作
    :return:
    """
    conn = pymysql.connect(
        host=MySQL_URL,
        port=MySQL_POST,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWD,
        db=MYSQL_DB,
        charset='utf8mb4')

    cur = conn.cursor()
    myConn_list = [conn, cur]
    return myConn_list


def close_MySQL(cur, conn):
    cur.close()
    conn.close()


def parse_page_index(text):
    """
    解析JSON数据
    :param text:
    :return:
    """
    try:
        data = json.loads(text)
        if data:
            return data
    except JSONDecodeError as e:
        print(e)
        return None


def save_to_mongodb(result, name):
    """
    数据保存到MongoDB
    :param result: 要保存的数据
    :param name: 表名称
    :return:
    """
    if db[name].insert(result):
        print_success('Successfully Saved to Mongodb')
        return True
    return False


def print_error(e):
    """
    打印错误
    :param e:
    :return:
    """
    try:
        print('\033[1;44m' + str(e) + '\033[0m')
    except Exception:
        print(e)


def print_success(e):
    """
    打印成功
    :param e:
    :return:
    """
    try:
        print('\033[1;35m' + str(e) + '\033[0m')
    except Exception:
        print(e)


def get_page_detail_get(url):
    """
    用讯代理（动态转发服务）爬取数据，详见http://www.xdaili.cn/transmit
    :param url:
    :return:返回网页数据
    """
    ip_port = ip + ":" + port

    _version = sys.version_info
    is_python3 = (_version[0] == 3)

    timestamp = str(int(time.time()))  # 计算时间戳
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

    if is_python3:
        string = string.encode()

    md5_string = hashlib.md5(string).hexdigest()  # 计算sign
    sign = md5_string.upper()  # 转换成大写
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {
        "Host": "47.95.13.233:81",
        "Referer": "http://www.cpopweixin.com/",
        "User-Agent": random.choice(USER_AGENTS),
        "Proxy-Authorization": auth
    }

    try:
        r = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        if r.status_code == 200:
            return r.text
        if r.status_code == 302 or r.status_code == 301:
            loc = r.headers['Location']
            time.sleep(1)
            r = requests.get(loc, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
            return r.text
        return None
    except Exception as e:
        print_error(e)
        return None


def get_page_detail_post(url, data):
    """
    用讯代理（动态转发服务）爬取数据，详见http://www.xdaili.cn/transmit
    :param url:
    :return:返回网页数据
    """
    _version = sys.version_info
    is_python3 = (_version[0] == 3)

    ip_port = ip + ":" + port

    timestamp = str(int(time.time()))  # 计算时间戳
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

    if is_python3:
        string = string.encode()

    md5_string = hashlib.md5(string).hexdigest()  # 计算sign
    sign = md5_string.upper()  # 转换成大写
    print(sign)
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

    print(auth)
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {"Proxy-Authorization": auth}
    r = requests.post(url, data=data,headers=headers, proxies=proxy, verify=False,
                     allow_redirects=False)
    return r.text


def getMongo_info_one(table, where):
    """
    获取mongodb中一条数据
    :param table: 查询的表
    :param where: 查询条件
    :return:
    """
    collection = db[table]
    cursor = collection.find_one(where)
    return cursor


def insert_mysql(cur, conn, sql):
    """
    执行SQL语句
    :param cur:
    :param conn:
    :param sql: SQL 语句
    :return:
    """
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print_error(e)


def get_UUID(str):
    """
    获取UUID 做唯一标识
    :param str:
    :return:
    """
    return uuid.uuid5(uuid.NAMESPACE_DNS, str)

