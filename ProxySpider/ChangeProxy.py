#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import collections
import re

proxyFile = "proxyFile.txt"
proxyList = []
curProxyIndex = 0
Proxy = collections.namedtuple("Proxy", ["ip", "port", "protocol"])
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}

#获取代理序列
def getProxyList():
    with open(proxyFile, "r") as f:
        while True:
            line = f.readline()
            if line is '':
                break
            line = line.split(" | ")
            proxyList.append(line)

#更换使用代理，IP和Port
def getProxy():
    global curProxyIndex
    if curProxyIndex >= len(proxyList):
        curProxyIndex = 0
    proxy = proxyList[curProxyIndex]
    curProxyIndex += 1
    return Proxy(proxy[0], proxy[1], proxy[3])

def testProxy():
    getProxyList()
    countNum = 100
    url = "http://www.ip111.cn/"
    for i in range(countNum):
        proxy = getProxy()
        p = proxy.protocol + "://" + proxy.ip + ":" + proxy.port
        proxies = {proxy.protocol : p}
        try:
            response = requests.get(url, proxies=proxies, headers=headers, timeout=5)
            if response.status_code != 200:
                print(response.status_code, response.text)
                continue
            soup = BeautifulSoup(response.text, "lxml")
            trs = soup.find("table", attrs={"class" : "table table-bordered"}).findAll("tr")
            tds = trs[1].findAll("td")
            info = tds[1].text.strip()
            print("Success : ", info)
        #except requests.HTTPError as e:
        except:
            print("Error : ", proxy.ip, proxy.port)
            continue
        time.sleep(2)

testProxy()