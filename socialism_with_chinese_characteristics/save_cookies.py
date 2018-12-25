from selenium import webdriver
import time
from store import PretreatMgr

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}
users = [["914138410@qq.com", "7944600578791113"],
         ["626591833@qq.com", "1913805949"],
         ["15757158496", "qwe.1995"],
         ["17816890851", "slz110120"]]


def login(username, password):
    browser = webdriver.Firefox(executable_path='geckodriver')
    browser.get(
        'https://passport.weibo.cn/signin/login?entry=mweibo&amp;res=wel&amp;wm=3349&amp;r=http%3A%2F%2Fm.weibo.cn%2F')
    browser.set_page_load_timeout(10)
    time.sleep(5)
    browser.find_element_by_id('loginName').send_keys(username)
    browser.find_element_by_id('loginPassword').send_keys(password)
    browser.find_element_by_id('loginAction').click()
    time.sleep(5)
    cookies = browser.get_cookies()
    browser.close()
    return cookies


if __name__ == '__main__':
    all_cookies = []
    for user in users:
        username, password = user[0], user[1]
        cookies = login(username, password)
        result = {}
        for item in cookies:
            try:
                result[item['name']] = item['value']
            except:
                continue
        all_cookies.append(result)
    PretreatMgr.save_file("user_cookies", "data", all_cookies)
