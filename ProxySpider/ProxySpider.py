#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import threading
import time
import http.client

proxyFile = open("proxyFile.txt", "w")
proxyAry = []
lock = threading.Lock()
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}

#找到代理列表
def getProxyList(url):
    countNum = 0
    '''
    pageNum = 0
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    pages = soup.find("div", attrs={"id" : "listnav"}).findAll("li")
    for page in pages:
        if page.find("a"):
            try:
                pageNum = int(page.find("a").text)
            except:
                continue
    '''
    pageNum = 100
    for index in range(1, pageNum+1):
        time.sleep(1.5)
        curUrl = url + str(index)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        table = soup.find("table", {"class" : "table table-bordered table-striped"})
        trs = table.findAll("tr")
        #首行为表头
        for tr in trs[1:]:
            tds = tr.findAll("td")
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            anomymous = tds[2].text.strip()
            protocol = tds[3].text.strip().lower()
            location = tds[4].text.strip()
            speed = tds[5].text.strip()
            verifiedTime = tds[6].text.strip()

            proxyAry.append([ip, port, anomymous, protocol, location, speed, verifiedTime])
            countNum += 1
    return countNum

#验证可用性
def verifyProxy():
    testUrl = "http://www.baidu.com/"
    while True:
        lock.acquire()
        if len(proxyAry) == 0:
            lock.release()
            break
        line = proxyAry.pop()
        lock.release()

        try:
            '''
            此方法验证不成功
            protocol = line[3] + "://" + line[0] + ":" + line[1]
            proxy = {line[3] : protocol}
            response = requests.get(testUrl, proxis=proxy, timeout=3)
            '''
            conn = http.client.HTTPConnection(line[0], line[1], timeout=5.0)
            conn.request(method = 'GET', url = testUrl, headers = headers )
            res = conn.getresponse()
            lock.acquire()
            line = " | ".join(line)
            line += "\n"
            proxyFile.write(line)
            lock.release()
        except:
            #代理不可用
            continue

if __name__ == "__main__":
    proxyFile.write("")
    proxyNum = getProxyList("https://www.kuaidaili.com/free/inha/")
    print("国内高匿：", proxyNum)

    print("验证代理有效性。。。。")

    allThread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxy)
        allThread.append(t)
        t.start()
    for t in allThread:
        t.join()
    
    proxyFile.close()
    print("验证完毕！")
