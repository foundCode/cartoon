# -*- coding: utf-8 -*-

import os
import urllib.request
import shutil

from utils import *


class Cartoon36mh:
    def __init__(self):
        self.home_url = 'https://36mh.com'
        self.browser_tool = BrowserTool()

    def search(self, keyword):
        url = self.home_url + '/search/'
        soup = get_soup(url, {'keywords': keyword})
        cartoon_li = soup.select('div[id="w0"]>ul>li>a')
        cartoon_urls = []
        cartoon_titles = []
        for cartoon in cartoon_li:
            cartoon_urls.append(cartoon['href'])
            cartoon_titles.append(cartoon['title'])
        return cartoon_urls, cartoon_titles

    def get_cartoon_data(self, cartoon_url):
        soup = get_soup(cartoon_url)
        cartoon_div = soup.select_one('div[class="book-cont cf"]')

        cartoon_image_url = cartoon_div.select_one('img[class="pic"]')['src']
        cartoon_title = cartoon_div.select_one('div[class="book-title"]>h1>span').get_text()

        return cartoon_image_url, cartoon_title

    def get_chapters(self, cartoon_url):
        soup = get_soup(cartoon_url)
        li_chapters = soup.select('ul[id="chapter-list-4"]>li>a')

        list_chapter = []
        urls = []
        for chapter in li_chapters:
            text = chapter.select_one('span').get_text()
            url = chapter['href']
            list_chapter.append(text)
            urls.append(self.home_url + url)

        return list_chapter, urls

    def get_chapter_data(self, chapter_url, page=1):
        page_source = self.browser_tool.get_page_source(chapter_url + '#p=%d' % page)
        soup = BeautifulSoup(page_source, 'lxml')

        div_image = soup.select_one('div[id="images"]')

        image_url = div_image.select_one('img')['src']
        now_section = div_image.select_one('img')['data-index']
        num_section = int(div_image.select_one('p').get_text().split('/')[1][:-1])

        return image_url, now_section, num_section

    def get_chapter_image_urls(self, chapter_url):
        home = requests.get(chapter_url, params=None, headers=get_headers())
        home.encoding = 'utf-8'
        html = home.text

        st = html.find('chapterImages = ') + len('chapterImages = ') + 2
        ed = html.find(';', st) - 2
        image_names = html[st: ed].split('","')

        st = html.find('chapterPath = ') + len('chapterPath = ') + 1
        ed = html.find(';', st) - 1
        pre_image_url = html[st: ed]

        # https://www.36mh.com/js/config.js
        image_urls = [('https://img001.yayxcc.com/' + pre_image_url + image_name) for image_name in image_names]

        return image_urls

    def get_chapter_image(self, chapter_url, start_page=1, num_load_page=-1):
        assert start_page >= 1
        assert num_load_page == -1 or num_load_page >= 1

        image_urls = self.get_chapter_image_urls(chapter_url)
        num_section = len(image_urls)
        start_page -= 1
        end_page = num_section
        if num_load_page != -1:
            end_page = min(end_page, start_page + num_load_page)
        images = []
        for page in range(start_page, end_page):
            images.append(get_image_by_url(image_urls[page]))

        return images

    def save_chapter(self, chapter_url, save_chapter_path):
        image_urls = self.get_chapter_image_urls(chapter_url)
        num_section = len(image_urls)
        for page in range(num_section):
            section_path = os.path.join(save_chapter_path, 'section_%d.jpg' % page)
            urllib.request.urlretrieve(image_urls[page], section_path)
            print('{} save to {}'.format(image_urls[page], section_path))

    # '/manhua/jushuowoshiwangdenver', r'F:\school\cartoon\据说我是王的女儿'
    def save_cartoon(self, cartoon_url, save_cartoon_path, start_chapter=1, num_load_chapter=-1):
        assert start_chapter >= 1
        assert num_load_chapter == -1 or num_load_chapter >= 1

        print('start {} save to {}'.format(cartoon_url, save_cartoon_path))

        if os.path.exists(save_cartoon_path) is False:
            os.mkdir(save_cartoon_path)
            print('create folder {}'.format(save_cartoon_path))

        chapters, urls = self.get_chapters(cartoon_url)
        num_chapters = len(chapters)

        start_chapter -= 1
        end_chapter = num_chapters
        if num_load_chapter != -1:
            end_chapter = min(end_chapter, start_chapter + num_load_chapter)

        for i in range(start_chapter, end_chapter):
            chapter_path = os.path.join(save_cartoon_path, validate_title(chapters[i]))
            if os.path.exists(chapter_path):
                shutil.rmtree(chapter_path)
            os.mkdir(chapter_path)
            print('create folder {}'.format(chapter_path))

            self.save_chapter(urls[i], chapter_path)


def main():
    cartoon36mh = Cartoon36mh()

    # print(cartoon36mh.get_chapter_image_urls('https://www.36mh.com/manhua/jushuowoshiwangdenver/175492.html'))

    cartoon36mh.save_cartoon(cartoon36mh.home_url + '/manhua/jushuowoshiwangdenver', r'F:\school\cartoon\据说我是王的女儿')

    # cartoon_urls, cartoon_titles = cartoon36mh.search('炎炎之消防队')
    #
    # cartoon_image_url, cartoon_title = cartoon36mh.get_cartoon_data(cartoon_urls[0])
    # print(cartoon_image_url, cartoon_title)
    # cartoon_image = get_image_by_url(cartoon_image_url)
    # cv2.imshow('cartoon_image', cartoon_image)
    # cv2.waitKey()

    # cartoon_url = cartoon_urls[0]
    # cartoon_title = cartoon_titles[0]
    # print(cartoon_url, cartoon_title)
    # chapters, chapter_urls = cartoon36mh.get_chapters(cartoon_url)
    # num_chapter = len(chapters)
    # for i in range(num_chapter):
    #     print(chapter_urls[i], chapters[i])
    #     images = cartoon36mh.get_chapter_image(chapter_urls[i], 1, num_load_page=2)
    #     for image in images:
    #         cv2.imshow('image', image)
    #         cv2.waitKey(0)


def test():
    url = 'https://www.36mh.com/manhua/jushuowoshiwangdenver/175492.html'
    home = requests.get(url, params=None, headers=get_headers(None))
    home.encoding = 'utf-8'
    html = home.text

    print(html)
    st = html.find('chapterImages = ')
    ed = html.find(';', st)
    print(st, ed)
    print(html[st + len('chapterImages = ') + 2: ed - 2])
    jpgs = html[st + len('chapterImages = ') + 2: ed - 2].split('","')
    for jpg in jpgs:
        print(jpg)

    st = html.find('chapterPath = ') + len('chapterPath = ') + 1
    ed = html.find(';', st) - 1
    pre_image_url = html[st: ed]
    print(pre_image_url)


if __name__ == '__main__':
    main()
    # test()
