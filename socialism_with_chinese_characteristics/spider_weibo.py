import requests
import time
from bs4 import BeautifulSoup
import json
from store import PretreatMgr
import numpy as np

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}


def get_ip():
    print("正在获取代理...")
    url = 'http://123.207.35.36:5010/get/'
    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    ip_port = soup.p.string
    print("代理抓取成功.")
    return ip_port


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


def spider(weiboid):
    PretreatMgr.save(weiboid=weiboid, datas=[])
    all_cookies = PretreatMgr.restore_file("user_cookies", "data")
    user_index = 0
    page = 0
    while True:
        if page % 5 == 0:
            proxies = get_proxies()
            user_index += 1
        session = get_session(user_index % len(all_cookies), all_cookies)
        vaild_page, html_none, change_ip = get_comments(page=page + 1, session=session, weiboid=weiboid,
                                                        proxies=proxies)
        if html_none:
            user_index += 1
            proxies = get_proxies()
            print("换人换ip,next_user_index=", user_index)
            continue
        if change_ip:
            proxies = get_proxies()
            print("连接失败跟换ip")
            continue
        if vaild_page:
            break
        else:
            page += 1
            time.sleep(30)


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


def get_comments(page, session, weiboid, proxies):
    vaild_page = False
    html_none = False
    change_ip = False
    try:
        html = session.get(
            'http://m.weibo.cn/single/rcList?format=cards&id={weiboid}&type=comment&hot=0&page={page}'.format(
                weiboid=weiboid, page=page), headers=headers, proxies=proxies, timeout=10).text
        try:
            js = json.loads(html)
            find_flag = False
            for j in js:
                if 'card_group' in j:
                    data = j['card_group']
                    datas = PretreatMgr.restore(weiboid=weiboid)
                    datas.append(data)
                    PretreatMgr.save(weiboid=weiboid, datas=datas)
                    print("page:", page, "  weibo_data:", data)
                    find_flag = True
            if find_flag is not True:
                vaild_page = True
        except:
            print("json解析失败")
            html_none = True
    except:
        change_ip = True
    session.close()
    return vaild_page, html_none, change_ip


if __name__ == '__main__':
    spider('4291814301557158')
