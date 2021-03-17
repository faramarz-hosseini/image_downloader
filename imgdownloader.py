import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
import os


class Scrapper:
    @staticmethod
    def get_img_link(img_tags):
        img_links = []
        for tag in img_tags:
            img_links.append(tag.get('src', None))
        return [link for link in img_links if link is not None]

    @staticmethod
    def create_folder(folder_name):
        if not os.path.exists(f'{folder_name}'):
            os.mkdir(f'{folder_name}')

    @staticmethod
    def get_extension(url):
        extensions = ['svg', 'jpg', 'png']
        for ext in extensions:
            if ext in url:
                return ext
        print('unsupported ext:', url)

    def download(self, url, img_links):
        folder_name = url.split(".")[1]
        file_name = 0
        for link in img_links:
            url = url + link if 'www' not in link else link
            ext = self.get_extension(link)
            if ext is None:
                continue
            file_address = f'{folder_name}/{file_name}.{ext}'
            try:
                urlretrieve(url, file_address)
                print('Downloaded:', file_address)
            except urllib.error.HTTPError:
                print('Download Failed:', file_address)
            file_name += 1

    @staticmethod
    def get_img_tags(url):
        web_source = urlopen(url).read()
        soup = BeautifulSoup(web_source, 'html.parser', from_encoding="iso-8859-1")
        return soup('img')

    def scrape(self, url):
        img_tags = self.get_img_tags(url)
        img_links = self.get_img_link(img_tags)
        self.create_folder(url.split('.')[1])
        self.download(url, img_links)


website_url = input('Enter URL: ')
Scrapper().scrape(website_url)
