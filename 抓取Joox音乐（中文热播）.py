# -*- coding: utf-8 -*-
# @Time    : 4/15/2020 9:41 PM
# @Author  : YenYoong
# @Website ：https://www.yybloger.com
# @File    : 抓取Joox音乐（中文热播）.py

'''
通过Xpath取到的信息：
//a[@class="jsx-2493651356"]/text() 歌曲名称
//a[@class="jsx-2493651356"]/@href  歌曲URL地址

歌曲地址URL：
https://api.joox.com/web-fcgi-bin/web_get_songinfo?songid=
'''

import requests
from lxml import etree
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}
url = "https://www.joox.com/my-en/chart/23"  # 中文热播榜URL

text = requests.get(url, headers=headers).text.encode('utf8')
# print(text)

dom = etree.HTML(text)
song_names = dom.xpath('//a[@class="jsx-2493651356"]/text()')
song_urls = dom.xpath('//a[@class="jsx-2493651356"]/@href')

for song_name, song_url in zip(song_names, song_urls):
    # print(song_name)
    # print(song_url)
    song_url_split = song_url.split('/')[3]  # 取到URL
    # print(song_url_split)
    # print(song_url_split)
    song_add_url = 'https://api.joox.com/web-fcgi-bin/web_get_songinfo?songid={}&singer_list=1&subscript=1&callback='.format(song_url_split)

    # print(song_add_url)
    time.sleep(0.01)

    song_base_url = requests.get(song_add_url, headers=headers).text
    decoded = json.loads(song_base_url)
    # print(decoded)
    mp3_url = decoded.get('m4aUrl')  # m4aUrl格式 / mp3Url格式

    # print(mp3_url)
    print(song_name)

    mp3 = requests.get(mp3_url, headers=headers).content  # MP3歌曲

    # 保存到当前目录Joox文件夹下
    with open('joox/{}.mp3'.format(song_name), 'wb') as f:
        f.write(mp3)
