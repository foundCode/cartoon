import re
import time
import requests
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


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
    # video = cv2.VideoCapture(image_url)
    # print(video.isOpened())
    # ret, image = video.read()

    # resp = urllib.request.urlopen(image_url)
    # image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
    # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # if np.ndim(image) == 3 and np.shape(image)[2] == 3:
    #     image = image[:, :, ::-1]

    response = requests.get(image_url)
    image = np.array(Image.open(BytesIO(response.content)), np.uint8)
    if np.ndim(image) == 3 and np.shape(image)[2] == 4:
        image = image[:, :, 0:3]
    elif np.ndim(image) == 2:
        image = np.tile(image[:, :, np.newaxis], [1, 1, 3])
    return image


class BrowserTool:
    def __init__(self, chrome_exe_path=r'resource\chromedriver_76.0.3809.68.exe'):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path=chrome_exe_path, chrome_options=option)

    def __del__(self):
        self.browser.quit()

    def get_page_source(self, url):
        self.browser.get(url)
        time.sleep(.5)
        return self.browser.page_source


class LRUCache:
    class Node:
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.previous = None
            self.next = None

    def remove_node(self, node):
        node.previous.next = node.next
        node.next.previous = node.previous
        node.previous = None
        node.next = None

    def add_node(self, node):
        node.next = self.head.next
        node.previous = self.head
        self.head.next.previous = node
        self.head.next = node

    def move_to_head(self, node):
        self.remove_node(node)
        self.add_node(node)

    def __init__(self, capacity=10, default_value=None):
        self.capacity = capacity
        self.default_value = default_value

        self.cache = {}
        self.head = self.Node()
        self.tail = self.Node()
        self.num_cache = 0

        self.head.next = self.tail
        self.head.previous = self.tail
        self.tail.previous = self.head
        self.tail.next = self.head

    def get(self, key):
        node = self.cache.get(key)
        if node is None:
            return self.default_value
        self.move_to_head(node)
        return node.value

    def put(self, key, value):
        node = self.cache.get(key)
        if node is not None:
            node.value = value
            self.move_to_head(node)
            return
        if self.num_cache == self.capacity:
            node = self.tail.previous
            self.cache.pop(node.key)
            self.remove_node(self.tail)
            self.tail = node
            self.num_cache -= 1
        node = self.Node(key, value)
        self.cache.update({key: node})
        self.add_node(node)
        self.num_cache += 1

    def popitem(self):
        if self.num_cache == 0:
            return
        node = self.tail.previous
        self.cache.pop(node.key)
        self.remove_node(self.tail)
        self.tail = node
        self.num_cache -= 1

    def pop(self, key):
        node = self.cache.get(key)
        if node is None:
            return
        self.cache.pop(key)
        self.remove_node(node)
        self.num_cache -= 1

    def is_cache(self, key):
        return self.cache.get(key) is not None
