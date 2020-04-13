import requests
from lxml import html
from selenium import webdriver
etree = html.etree


def download(src, movie_name, path):
    poster_loc = path + '/' + str(movie_name) + '.jpg'
    # 获取图片信息
    try:
        poster = requests.get(src, timeout=10)
    except requests.exceptions.ConnectionError:
        print('图片无法下载')
    # 传入本地文件中
    fp = open(poster_loc, 'wb')
    fp.write(poster.content)
    fp.close()

browser = webdriver.Chrome()

# 电影明星‘name’的共n页豆瓣海报存到‘path’
def douban_reptile(name, n, path):
    for j in range(0, 15*n, 15):
        # 打开第j页演员电影信息浏览器
        browser.get('https://movie.douban.com/subject_search?search_text=' + name + '&cat=1002&start=' + str(j))
        html = etree.HTML(browser.page_source)
        # 获取海报XPath并将所有该Xpath的src传入字典
        poster_xpath = "//div[@class='item-root']/a[@class='cover-link']/img[@class='cover']/@src"
        posters = html.xpath(poster_xpath)
        # 获取电影名称XPath
        movieName_xpath = "//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']"
        movieNames = html.xpath(movieName_xpath)
        # 更改图片和文字格式
        for poster, movieName in zip(posters, movieNames):
            poster = poster.replace('webp', 'jpg')
            movieName.text = movieName.text.replace('?', '')
            download(poster, movieName.text, path)
    print("下载完成")
    browser.close()


if __name__ == '__main__':
    douban_reptile('周星驰', 3, 'C:/Users/郭勇啸/Desktop/海报')