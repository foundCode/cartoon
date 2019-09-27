# -*- coding: utf-8 -*-
import cv2
import time
import queue
import threading

from cartoon_crawler.cartoon_36mh import Cartoon36mh
from tools.utils import get_image_by_url
from tools.utils import LRUCache


def get_init_image():
    return cv2.imread(r'resource\init_image.png')[:, :, ::-1]


class CacheImage(threading.Thread):
    def __init__(self, max_cache=10, max_preloading=10):
        threading.Thread.__init__(self)
        self.max_preloading = max_preloading

        self.url_queue = queue.Queue()
        self.preloading_image = {}
        self.loading_url = None
        self.num_preloading = 0

        self.cache_image = LRUCache(max_cache)
        self.exit = False

    def run(self):
        while not self.exit:
            if self.url_queue.empty() or self.num_preloading >= self.max_preloading or self.loading_url is not None:
                time.sleep(1.)
                continue
            image_url = self.url_queue.get_nowait()
            if self.is_cache(image_url):
                continue
            print('start preloading')
            self.loading_url = image_url
            image = get_image_by_url(image_url)
            self.preloading_image.update({image_url: image})
            self.num_preloading += 1
            self.loading_url = None
            print('preload done!!!', image_url)
        print('CacheImage stop!!!')

    def clear_preload(self):
        self.url_queue.queue.clear()
        self.preloading_image.clear()
        self.num_preloading = 0

    def update_url(self, urls):
        for url in urls:
            self.url_queue.put_nowait(url)

    def load_image(self, image_url):
        while self.loading_url == image_url:
            time.sleep(.2)
        image = self.preloading_image.get(image_url)
        if image is not None:
            self.preloading_image.pop(image_url)
            self.num_preloading -= 1
            self.cache_image.put(image_url, image)
            return
        print('preloading image is none')
        if self.cache_image.is_cache(image_url):
            return
        print('cache image is none')
        self.loading_url = image_url
        image = get_image_by_url(image_url)
        print('get_image_by_url', image_url)
        if self.is_cache(image_url) is False:
            self.cache_image.put(image_url, image)
        self.loading_url = None

    def get_image(self, image_url):
        self.load_image(image_url)
        return self.cache_image.get(image_url)

    def is_cache(self, image_url):
        return self.preloading_image.get(image_url) is not None or self.cache_image.is_cache(image_url)

    def close(self):
        self.exit = True


class LoadCartoon:
    CURRENT_FRAGMENT = -1
    PREVIOUS_FRAGMENT = -2
    NEXT_FRAGMENT = -3

    def __init__(self):
        self.cartoon_36mh = Cartoon36mh()
        self.cartoon_titles = []
        self.cartoon_urls = []
        self.cartoon_index = -1

        self.cartoon_image_url = None
        self.cartoon_image = None

        self.chapter_titles = []
        self.chapter_urls = []
        self.chapter_index = -1
        self.num_chapter = -1

        self.fragment_image_urls = []
        self.fragment_index = -1
        self.num_fragment = -1

        self.cache_image = CacheImage()
        self.cache_image.start()

    def init_cartoon(self):
        self.cartoon_index = -1
        self.num_chapter = -1
        self.cartoon_image_url = None
        self.chapter_titles = []
        self.chapter_urls = []
        self.init_chapter()

    def init_chapter(self):
        self.chapter_index = -1
        self.fragment_image_urls = []
        self.cache_image.clear_preload()
        self.fragment_index = -1
        self.num_fragment = -1

    def search(self, search_text):
        if len(search_text) == 0:
            return []
        print(search_text)
        self.cartoon_urls, self.cartoon_titles = self.cartoon_36mh.search(search_text)
        self.cartoon_index = -1
        print('num_cartoon =', len(self.cartoon_titles))

    def select_cartoon(self, cartoon_index):
        assert 0 <= cartoon_index < len(self.cartoon_titles)
        if self.cartoon_index == cartoon_index:
            return
        self.init_cartoon()
        self.cartoon_index = cartoon_index
        cartoon_title, cartoon_url = self.cartoon_titles[self.cartoon_index], self.cartoon_urls[self.cartoon_index]
        print(cartoon_title, cartoon_url)
        self.cartoon_image_url, _ = self.cartoon_36mh.get_cartoon_data(cartoon_url)

        self.chapter_titles, self.chapter_urls = self.cartoon_36mh.get_chapters(cartoon_url)

        self.num_chapter = len(self.chapter_titles)
        self.load_cartoon_image()
        print('num_chapter =', self.num_chapter)

    def select_chapter(self, chapter_index):
        assert 0 <= chapter_index < self.num_chapter
        if self.chapter_index == chapter_index:
            return
        self.init_chapter()
        self.chapter_index = chapter_index
        chapter_title, chapter_url = self.chapter_titles[self.chapter_index], self.chapter_urls[self.chapter_index]
        print(chapter_title, chapter_url)
        self.fragment_image_urls = self.cartoon_36mh.get_chapter_image_urls(chapter_url)

        self.cache_image.update_url(self.fragment_image_urls)

        self.fragment_index = 0
        self.num_fragment = len(self.fragment_image_urls)

        print('num_fragment =', self.num_fragment)

    def load_cartoon_image(self):
        if self.cartoon_image_url is None:
            self.cartoon_image = None
            return
        self.cartoon_image = get_image_by_url(self.cartoon_image_url)

    def get_cartoon_title_url(self):
        if self.cartoon_index == -1:
            return None
        cartoon_title, cartoon_url = self.cartoon_titles[self.cartoon_index], self.cartoon_urls[self.cartoon_index]
        title_url = {'title': cartoon_title, 'url': cartoon_url}
        return title_url

    def get_chapter_title_url(self):
        if self.chapter_index == -1:
            return None
        chapter_title, chapter_url = self.chapter_titles[self.chapter_index], self.chapter_urls[self.chapter_index]
        title_url = {'title': chapter_title, 'url': chapter_url}
        return title_url

    def get_cartoon_image(self):
        if self.cartoon_image is None:
            self.load_cartoon_image()
        return self.cartoon_image

    def get_fragment_image(self, fragment_index=CURRENT_FRAGMENT):
        if fragment_index == self.CURRENT_FRAGMENT:
            return self.get_current_fragment_image()
        elif fragment_index == self.PREVIOUS_FRAGMENT:
            return self.get_previous_fragment_image()
        elif fragment_index == self.NEXT_FRAGMENT:
            return self.get_next_fragment_image()
        elif fragment_index >= 0:
            return self.get_current_fragment_image(fragment_index)
        return None

    def get_previous_fragment_image(self):
        if self.fragment_index == -1:
            return None
        if self.fragment_index > 0:
            self.fragment_index -= 1
        else:
            if self.chapter_index > 0:
                self.select_chapter(self.chapter_index - 1)
                self.fragment_index = self.num_fragment - 1
            else:
                return None
        return self.get_current_fragment_image()

    def get_current_fragment_image(self, fragment_index=-1):
        assert fragment_index == -1 or fragment_index >= 0
        if self.fragment_index == -1 or fragment_index >= self.num_fragment:
            return None
        if fragment_index != -1:
            self.fragment_index = fragment_index
        image_url = self.fragment_image_urls[self.fragment_index]
        print('fragment_index =', self.fragment_index, image_url)
        image = self.cache_image.get_image(image_url)
        return image

    def get_next_fragment_image(self):
        if self.fragment_index == -1:
            return None
        if self.fragment_index + 1 < self.num_fragment:
            self.fragment_index += 1
        else:
            if self.chapter_index + 1 < self.num_chapter:
                self.select_chapter(self.chapter_index + 1)
            else:
                return None
        return self.get_current_fragment_image()

    def close(self):
        self.cache_image.close()
        # self.cache_image.join()
