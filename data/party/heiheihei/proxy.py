import requests
from bs4 import BeautifulSoup
import random
import time
from Download import request
from config import ipList, userAgentList

class download:
    def __init__(self):

    	## shit! 好ip用不了了
        #self.iplist = []
        #html = requests.get('http://haoip.cc/tiqu.htm')
       # soup = BeautifulSoup(html.text,'lxml')
       # iplistn =soup.find('div',class_='col-xs-12').get_text().split()
       # for i in iplistn:
       #     self.iplist.append(i)


       	##临时创个ip列表
       	self.iplist = ipList
        self.user_agent = userAgentList

    def get(self,url,timeout=10,num_retries=5):
        print('开始获取：',url)
        UA = random.choice(self.user_agent)
        headers = {'User-Agent':UA}
        try:
            IP = ''.join(str(random.choice(self.iplist)).strip())
            proxy = {'http':IP}
            return requests.get(url,headers=headers,proxies=proxy,timeout=timeout)
        except :
            if num_retries > 0:
                print('获取失败，10s后重新获取，剩余尝试次数：',num_retries)
                time.sleep(10)
                return self.get(url,timeout,num_retries-1)
            else:
                print('代理不好使了！取消代理')
                return request.get(url)


request_with_proxy = download()

