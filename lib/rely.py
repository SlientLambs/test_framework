# TODO: 处理测试依赖数据
import re
import libs.psycopg2 as psycopg2
from bin.config import DATABASE


def _get_query_data(sql):
    """
    查询数据库数据
    :param sql:数据执行语句
    :return:返回查询的数据
    """
    global data
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return data


def get_headers(username):
    """
    获取访问接口所需的token
    :param username: 所需要获取token的用户名
    :return: 包含token的头部信息
    """
    sql = """
    SELECT t.token
    FROM sys_user_token t
    LEFT JOIN sys_user u
    ON t.user_id=u.user_id
    WHERE u.username='%s';
    """ % username
    try:
        token = _get_query_data(sql)[0][0]
    except IndexError:
        token = ''
    headers = {
            'Host': '192.168.0.238',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/78.0.3904.97 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'http://192.168.0.238/repaire/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    return headers


def get_user_list():
    """
    获取系统用户名列表，用于判断获取谁的token
    :return: 由系统用户名组成的列表
    """
    sql = """
        SELECT username
        FROM sys_user;
        """
    name = _get_query_data(sql)
    users = []
    for n in name:
        users.append(n[0])
    return users


def form_data(test_data):
    """
    构造需要通过SQL语句动态生成的测试数据
    :param test_data: 包含SQL语句的测试数据
    :return: 通过执行SQL语句并将原SQL语句位置进行替换后测试数据
    """
    rule = re.compile(r'\$([se])\{(.+?)\}')
    for k, v in rule.findall(test_data):
        if k == 's':
            value = _get_query_data(v)[0][0]
            value = str(value)
            test_data = rule.sub(value, test_data, 1)
        elif k == 'e':
            test_data = []
            except_check = v.split('&')[0]
            actual_check = _get_query_data(v.split("&")[1])[0][0]
            test_data.append(except_check)
            test_data.append(actual_check)
    return test_data


def form_params(raw_params):
    """
    用于将query params中的中文进行URL转码
    :param raw_params: 未处理的query params
    :return: 已处理好的query params
    """
    cooked_params = {}
    try:
        for i in raw_params.split('&'):
            key, value = i.split('=')
            dict_t = {key: value}
            cooked_params.update(dict_t)
    except ValueError:
        cooked_params = ''
    return cooked_params
