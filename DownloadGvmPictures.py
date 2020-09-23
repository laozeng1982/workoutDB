import os
import re
import shutil
import time

import urllib3
from selenium import webdriver

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/1 7.0.963.56 Safari/535.11"
path = "D:\\fitness"
headers = {"User-Agent": agent}
GoogleChromeLocation = "C:/Program Files (x86)/Google/Chrome/Application"
BaseUrl = "https://weighttraining.guide/category/exercises/page"


def findRightDriver():
    driver = None
    chop = webdriver.ChromeOptions()
    # chop.add_extension('AdBlock_v3.9.5.crx')
    try:
        driver = webdriver.Chrome(chrome_options=chop)
    except Exception as e:
        print(e)

        import xml.dom.minidom

        chromeFile = os.path.join(GoogleChromeLocation, "chrome.VisualElementsManifest.xml")
        version = None
        if os.path.exists(chromeFile):
            dom = xml.dom.minidom.parse(chromeFile)
            root = dom.documentElement
            for node in root.getElementsByTagName('VisualElements'):
                print(node.getAttribute('Square150x150Logo'))
                version = node.getAttribute('Square150x150Logo').split('.')[0]
                print("Current Chrome Version: ", version)

        if version:
            driverPath = '.\\chromedrivers\\chromedriver%s.exe' % version

            print(os.path.abspath(driverPath))
            if os.path.exists(driverPath):
                print("find right chrome driver!")
                shutil.copyfile('.\\chromedrivers\\chromedriver%s.exe' % version, '.\\chromedriver.exe')
                driver = webdriver.Chrome(chrome_options=chop)
            else:
                print("does not find right chrome driver!")
                driver = None
    finally:
        return driver


def saveGymVisualJPGs():
    baseUrl = "https://www.gymvisual.com/3-illustrations?p="

    driver = findRightDriver()
    directory = "D:\\gym-visual"
    if not os.path.exists(directory):
        os.mkdir(directory)

    if driver:
        driver.maximize_window()
        for idx in range(186, 187):
            driver.get(baseUrl + str(idx))
            print("Page %3d, Url: %s" % (idx, baseUrl + str(idx)))
            try:
                imageItems = driver.find_elements_by_class_name("product_img_link")

                for item in imageItems:
                    title = item.get_property('title')
                    subItems = item.find_element_by_tag_name("img")

                    imageUrl = subItems.get_property('src')
                    print("%-60s: %s" % (title, imageUrl))
                    urllib3.disable_warnings()
                    http = urllib3.PoolManager()
                    request = http.request('GET', imageUrl.replace("catalog", "large"), headers=headers)
                    imageData = request.data

                    fileName = os.path.join(directory, imageUrl.split("/")[-1])

                    with open(fileName, "wb") as f:
                        f.write(imageData)

            except Exception as e:
                print(e)
            finally:
                time.sleep(1)


def saveGymVisualGifs():
    baseUrl = "https://www.gymvisual.com/16-animated-gifs?p="

    driver = findRightDriver()
    directory = "D:\\gym-visual\\gif"
    if not os.path.exists(directory):
        os.mkdir(directory)

    if driver:
        driver.maximize_window()
        for idx in range(74, 175):
            driver.get(baseUrl + str(idx))
            print("Page %3d, Url: %s" % (idx, baseUrl + str(idx)))
            try:
                imageItems = driver.find_elements_by_class_name("product_img_link")

                for count, item in enumerate(imageItems):
                    title = item.get_property('title')
                    subItems = item.find_element_by_tag_name("img")

                    imageUrl = subItems.get_property('src')
                    print("%-3d, %-60s: %s" % ((idx - 1) * 20 + count + 1, title, imageUrl))
                    urllib3.disable_warnings()
                    http = urllib3.PoolManager()
                    request = http.request('GET', imageUrl, headers=headers)
                    imageData = request.data

                    fileName = os.path.join(directory, '-'.join(title.replace('/', '-').split(' ')) + '.gif')

                    with open(fileName, "wb") as f:
                        f.write(imageData)

            except Exception as e:
                print(e)
            finally:
                time.sleep(1)


class ImageSpider(object):
    """
    Image Spider from weighttraining.guide
    """

    def __init__(self):
        self.Count = 0
        pass

    def saveAllImage(self, imageUrl: str):
        """

        :param imageUrl:
        :return:
        """
        print("imageUrl", imageUrl)
        http = urllib3.PoolManager()
        request = http.request('GET', imageUrl, headers=headers)
        imageData = request.data

        fileName = os.path.join(path, imageUrl.split("/")[-1])

        print("fileName", fileName)
        with open(fileName, "wb") as f:
            f.write(imageData)

        print('Saving: ', fileName)

        time.sleep(0.1)

    def saveBigImage(self, imageUrl: str):
        """

        :param imageUrl:
        :return:
        """
        # print("imageUrl", imageUrl)
        b = imageUrl.rfind("-")
        bigImageUrl = imageUrl[:b] + ".png"
        fileName = os.path.join(path, bigImageUrl.split("/")[-1])

        if not os.path.exists(fileName):
            urllib3.disable_warnings()
            http = urllib3.PoolManager()
            request = http.request('GET', bigImageUrl, headers=headers)
            imageData = request.data

            with open(fileName, "wb") as f:
                f.write(imageData)
            self.Count += 1
            print("%s, fileName:%s" % (self.Count, fileName))

            time.sleep(0.1)

    def getImageFormUrl(self, url):
        """

        :param url:
        :return:
        """
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        request = http.request('GET', url, headers=headers)
        # print(request.status)
        # print(type(request.data))
        # print(type(request.data.decode('utf-8')))
        textHtml = request.data.decode('utf-8')
        # print(textHtml)
        p1 = r'(https:.*?.png)'
        pattern = re.compile(p1)
        images = pattern.findall(textHtml)

        for img in images:
            if " " not in img and "https:\\" not in img:
                # print(img)
                self.saveBigImage(img)

    def saveImagePageRange(self, fromPage: int, toPage: int):
        """

        :param fromPage:
        :param toPage:
        :return:
        """

        if not os.path.exists(path):
            os.system('mkdir %s' % path)

        idx = fromPage
        while idx <= toPage:
            url = "%s/%s/" % (BaseUrl, idx)
            # print(url)

            print("\nPage: %d" % idx)

            self.getImageFormUrl(url)
            idx += 1


if __name__ == '__main__':
    # findLiuLianRealUrl()
    saveGymVisualGifs()
    pass
