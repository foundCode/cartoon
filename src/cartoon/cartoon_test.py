# -*- coding: utf-8 -*-

from cartoon_36mh import Cartoon36mh
from utils import get_image_by_url


class LoadCartoon:
    def __init__(self):
        self.cartoon_36mh = Cartoon36mh()
        self.cartoon_title_url = []
        self.cartoon_index = -1

        self.cartoon_image_url = None

        self.chapter_title_url = []
        self.chapter_index = -1
        self.num_chapter = -1

        self.fragment_image_urls = []
        self.fragment_index = -1
        self.num_fragment = -1

    def init_cartoon(self):
        self.cartoon_index = -1
        self.num_chapter = -1
        self.cartoon_image_url = None
        self.init_chapter()

    def init_chapter(self):
        self.chapter_title_url = []
        self.chapter_index = -1
        self.init_fragment()

    def init_fragment(self):
        self.fragment_image_urls = []
        self.fragment_index = -1
        self.num_fragment = -1

    def search(self, search_text):
        if len(search_text) == 0:
            return []
        cartoon_urls, cartoon_titles = self.cartoon_36mh.search(search_text)
        print(cartoon_urls)
        self.cartoon_title_url.clear()
        num_cartoon = len(cartoon_urls)
        for i in range(num_cartoon):
            self.cartoon_title_url.append({'title': cartoon_titles[i], 'url': cartoon_urls[i]})
        return cartoon_titles

    def select_cartoon(self, cartoon_index):
        assert 0 <= cartoon_index < len(self.cartoon_title_url)
        self.init_chapter()
        self.cartoon_index = cartoon_index
        title_url = self.cartoon_title_url[self.cartoon_index]
        print(title_url)
        cartoon_title, cartoon_url = title_url['title'], title_url['url']
        self.cartoon_image_url, _ = self.cartoon_36mh.get_cartoon_data(cartoon_url)

        chapter_titles, chapter_urls = self.cartoon_36mh.get_chapters(cartoon_url)

        self.chapter_title_url.clear()
        self.num_chapter = len(chapter_urls)
        for i in range(self.num_chapter):
            self.chapter_title_url.append({'title': chapter_titles[i], 'url': chapter_urls[i]})

        print('num_chapter =', self.num_chapter)

    def select_chapter(self, chapter_index):
        assert 0 <= chapter_index < self.num_chapter
        self.init_fragment()
        self.chapter_index = chapter_index
        title_url = self.chapter_title_url[self.chapter_index]
        print(title_url)
        chapter_title, chapter_url = title_url['title'], title_url['url']
        self.fragment_image_urls = self.cartoon_36mh.get_chapter_image_urls(chapter_url)

        self.fragment_index = 0
        self.num_fragment = len(self.fragment_image_urls)

        print('num_fragment =', self.num_fragment)

    def get_cartoon_title_url(self):
        if self.cartoon_index == -1:
            return None, None
        title_url = self.cartoon_title_url[self.cartoon_index]
        return title_url['title'], title_url['url']

    def get_chapter_title_url(self):
        if self.chapter_index == -1:
            return None, None
        title_url = self.chapter_title_url[self.chapter_index]
        return title_url['title'], title_url['url']

    def get_cartoon_image(self):
        if self.cartoon_image_url is None:
            return None
        return get_image_by_url(self.cartoon_image_url)

    def get_previous_fragment_image(self):
        if self.fragment_index == -1:
            return None
        if self.fragment_index > 0:
            self.fragment_index -= 1
        else:
            if self.chapter_index > 0:
                self.chapter_index -= 1
                self.select_chapter(self.chapter_index)
            else:
                return None
        return self.get_current_fragment_image()

    def get_current_fragment_image(self, fragment_index=-1):
        assert fragment_index == -1 or 0 <= fragment_index < self.num_fragment
        if self.fragment_index == -1:
            return None
        if fragment_index != -1:
            self.fragment_index = fragment_index
        image_url = self.fragment_image_urls[self.fragment_index]
        print('fragment_index =', self.fragment_index, image_url)
        return get_image_by_url(image_url)

    def get_next_fragment_image(self):
        if self.fragment_index == -1:
            return None
        if self.fragment_index + 1 < self.num_fragment:
            self.fragment_index += 1
        else:
            if self.chapter_index + 1 < self.num_chapter:
                self.chapter_index += 1
                self.select_chapter(self.chapter_index)
            else:
                return None
        return self.get_current_fragment_image()


def main():
    import cv2
    load_cartoon = LoadCartoon()
    load_cartoon.search('天空')
    load_cartoon.select_cartoon(0)
    load_cartoon.select_chapter(0)
    image = load_cartoon.get_current_fragment_image()
    cv2.imshow('image', image)
    cv2.waitKey()
    image = load_cartoon.get_previous_fragment_image()
    if image is not None:
        print('image is none')
        cv2.imshow('image', image)
        cv2.waitKey()
    while True:
        opt = input('input = ')
        if opt == 'p':
            image = load_cartoon.get_previous_fragment_image()
        elif opt == 'n':
            image = load_cartoon.get_next_fragment_image()
        elif opt == 'c':
            image = load_cartoon.get_current_fragment_image()
        elif opt.isnumeric():
            image = load_cartoon.get_current_fragment_image(int(opt))
        if image is None:
            break
        cv2.imshow('image', image)
        cv2.waitKey()


if __name__ == '__main__':
    main()
