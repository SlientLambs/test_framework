# TODO: 接口自动化框架配置文件
import os

# HOST地址
HOST = 'http://server.penbox.top:8088'

# 文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data/')
TESTCASE_DIR = os.path.join(BASE_DIR, 'cases/')
REPORT_DIR = os.path.join(BASE_DIR, 'report')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'bin/template.txt')

# 登录请求头部
HEADERS = {
            'Host': 'server.penbox.top:8088',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

# 数据库数据
DATABASE = {
    'host': '数据库地址',
    'port': '数据库端口号',
    'user': '数据库登录名',
    'password': '数据库密码',
    'database': '数据库名称'
}
