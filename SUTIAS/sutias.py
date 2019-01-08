import logging

import requests

requests.packages.urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO)


class SUTIAS:
    MY_URL = 'https://lab.yuangezhizao.cn/SUTIAS'
    ACTION_METHOD = 'ac_portal/login.php'

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.session = requests.session()

    def find_login_page(self):
        logging.info('检查网络状态')
        r = self.session.get(self.MY_URL, allow_redirects=False, verify=False)
        if r.status_code == 302:
            logging.info('未在线')
            return r.headers['Location'].split('ac_portal')[0]
        else:
            logging.info('已在线')
            return 0

    def login(self):
        location = self.find_login_page()
        if not location:
            return logging.info('无需登录')
        with open('./location.txt', 'wb') as f:
            f.write(location.encode())
        data = {
            'opr': 'pwdLogin',
            'userName': self.username,
            'pwd': self.password,
            'rememberPwd': 1
        }
        r = self.session.post(location + self.ACTION_METHOD, data=data)
        r.encoding = 'utf-8'
        logging.info(r.text)
        if 'true' in r.text:
            logging.info('登录成功')
        else:
            logging.info('登录失败')

    def logout(self):
        if self.find_login_page():
            return logging.info('无需注销')
        with open('./location.txt') as f:
            location = f.read()
        data = {
            'opr': 'logout',
        }
        r = self.session.post(location + self.ACTION_METHOD, data=data)
        r.encoding = 'utf-8'
        logging.info(r.text)
        if 'true' in r.text:
            logging.info('注销成功')
        else:
            logging.info('注销失败')
