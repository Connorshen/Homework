import requests
from bs4 import BeautifulSoup
import json
from store import PretreatMgr
import sqlite3
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}
key_for_info = ["昵称", "性别", "地区", "生日"]


def get_ip():
    print("正在获取代理...")
    url = 'http://123.207.35.36:5010/get/'
    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    ip_port = soup.p.string
    print("代理抓取成功.")
    return ip_port


def check_ip(ip_port):
    proxies = {
        "http": "http://{ip_port}".format(ip_port=ip_port),  # 代理ip
        "ssl": "http://{ip_port}".format(ip_port=ip_port)  # 代理ip
    }
    try:
        sess = requests.session()
        html = sess.get("http://httpbin.org/ip", proxies=proxies, timeout=5).text
        sess.close()
        js = json.loads(html)
        print("check_ip_success:", js)
        return True
    except:
        return False


def get_session(user_index, all_cookies):
    cookies = all_cookies[user_index]
    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookies)
    return session


def get_proxies():
    while True:
        ip_port = get_ip()
        if check_ip(ip_port):
            proxies = {
                "http": "http://{ip_port}".format(ip_port=ip_port),  # 代理ip
                "ssl": "http://{ip_port}".format(ip_port=ip_port)  # 代理ip
            }
            return proxies
        else:
            print("check_ip_failed,开始获取新ip")


# ["昵称", "性别", "地区", "生日"]
def get_profile(session, userid, proxies):
    change_ip = False
    spider_success = False
    invalid_id = False
    try:
        html = session.get(
            'https://weibo.cn/{userid}/info'.format(
                userid=userid), headers=headers, timeout=10, proxies=proxies).text
        mainSoup = BeautifulSoup(html, 'lxml')
        divs = mainSoup.find_all("div")
        info_div = None
        for div in divs:
            if div.previous_element == "基本信息":
                info_div = div
        if info_div is not None:
            useful_info = [str(c) for c in info_div.contents if str(c) != "<br/>"]
            profile_dict = {}
            for info in useful_info:
                info = info.split(":")
                if info[0] in key_for_info:
                    index = key_for_info.index(info[0])
                    if 0 <= index < len(key_for_info):
                        profile_dict[key_for_info[index]] = info[1]
            ls = [None, None, None, None]
            for i in range(len(key_for_info)):
                if profile_dict.get(key_for_info[i]):
                    ls[i] = profile_dict[key_for_info[i]]
            profile = Profile(userid, ls[0], ls[1], ls[2], ls[3])
            insert(profile)
            spider_success = True
        else:
            if html != "":
                invalid_id = True
    except:
        change_ip = True
    return change_ip, spider_success, invalid_id


def spider(ids):
    all_cookies = PretreatMgr.restore_file("user_cookies", "data")
    user_index = 0
    proxies = get_proxies()
    success_time = 0
    for user_id in ids:
        if len(find(user_id)) == 0:
            while True:
                if success_time % 8 == 0:
                    proxies = get_proxies()
                    user_index += 1
                session = get_session(user_index % len(all_cookies), all_cookies)
                change_ip, spider_success, invalid_id = get_profile(session, user_id, proxies)
                if invalid_id:
                    print("无效id，开始取下一个id")
                    break
                if spider_success:
                    print("get_profile_success")
                    success_time += 1
                    break
                else:
                    if change_ip:
                        print("need_change_ip")
                        proxies = get_proxies()
                    else:
                        user_index += 1
                        print("换人，current_index:", user_index)
            time.sleep(5)
        else:
            print("该user已经爬取过")


class Profile:
    def __init__(self, userid, username, sex, location, birthday):
        self.userid = userid
        self.username = username
        self.sex = sex
        self.location = location
        self.birthday = birthday


def init_data_base():
    conn = sqlite3.connect("database/user_info.db")
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE user (id varchar(20) primary key, username varchar(20),sex varchar(20),location varchar(20),birthday varchar(20))')
    cursor.close()
    conn.commit()
    conn.close()


def insert(profile):
    conn = sqlite3.connect("database/user_info.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user VALUES ('{id}','{username}','{sex}','{location}','{birthday}')".format(id=profile.userid,
                                                                                                 username=profile.username,
                                                                                                 sex=profile.sex,
                                                                                                 location=profile.location,
                                                                                                 birthday=profile.birthday))
    cursor.close()
    conn.commit()
    conn.close()


def find(userid):
    conn = sqlite3.connect("database/user_info.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id = {id}".format(id=userid))
    result = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return result


if __name__ == '__main__':
    user_ids = PretreatMgr.restore_file("weibo_users", "user_ids")
    spider(user_ids)
