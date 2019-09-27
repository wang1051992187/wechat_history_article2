import os
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
]


# 讯代理平台
orderno = ""
secret = ""
ip = "forward.xdaili.cn"
port = "80"

# 若快打码平台
ruokuai_name = "w1051992187"
ruokuai_pswd = ""
ruokuai_soft_id = ""
ruokuai_soft_key = ""

# 易源数据API
SHOWAPI_APPID = ''
SHOWAPI_SECRET = ''

# Mongo
MONGO_URL = '192.168.1.108'
MONGO_DB = 'wechat_update'

# MySQL
MySQL_URL = '192.168.10.81'
MySQL_POST = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = ''
MYSQL_DB = ''

MYSQL_TABLE_WECHAT_INFO = ''

# 是否备份数据库
IS_BACK_UP = True
# 备份数据库
MYSQL_TABLE_WECHAT_INFO_2 = 'wechat_article_update'

# 文章关键词提取 
KEYWORDS_URL = 'http://192.168.1.44:5000/keywords'
# 默认去取前20个
TOP_NUM = 20
# 文章摘要提取 
SUMMARY_URL = 'http://192.168.1.44:5000/summary'
# 文章摘要 默认 length_rate
RATE = "0.2"

# 银行文件
BANK_FILE = os.path.abspath(os.path.dirname(__file__)) + '/bank_all.txt' # Linux 绝对地址
# BANK_FILE = 'bank_all.txt'

# 设置爬取前多久的数据（24小时）
BEFORE_TIME = 24 * 60 * 60


