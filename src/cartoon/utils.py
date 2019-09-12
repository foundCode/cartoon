import re
import time
import requests
import urllib.request
import cv2
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup


def validate_title(title):
    rstr = r'[\/\\\:\*\?\"\<\>\|]'  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, '', title)
    return new_title


def cookie_to_string(cookies):
    return ';'.join([key + '=' + value for key, value in cookies.items()])


def get_headers(cookies=None):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                  'q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; '
                      'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    if cookies is not None:
        headers['cookie'] = cookie_to_string(cookies)
    return headers


def get_soup(url, params=None, cookies=None):
    home = requests.get(url, params=params, headers=get_headers(cookies))
    home.encoding = 'utf-8'
    soup = BeautifulSoup(home.text, 'lxml')
    return soup


def get_image_by_url(image_url):
    resp = urllib.request.urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
    # B G R
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


class BrowserTool:
    def __init__(self, chrome_exe_path=r'.\chromedriver_76.0.3809.68.exe'):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path=chrome_exe_path, chrome_options=option)

    def __del__(self):
        self.browser.quit()

    def get_page_source(self, url):
        self.browser.get(url)
        time.sleep(.5)
        return self.browser.page_source
