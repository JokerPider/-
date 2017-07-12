import requests
from bs4 import BeautifulSoup
import random
import time
from config import ipList, userAgentList


class download:
    def __init__(self):
    	#self.iplist = []
    	#html = requests.get('http://haoip.cc/tiqu.htm')
    	#soup = BeautifulSoup(html.text,'lxml')
    	#iplistn = soup.find('div',class_='col-xs-12').get_text().split()
    	#for i in iplistn:
    	#	self.iplist.append(i)

    	self.iplist = ipList
    	self.user_agents = userAgentList

    def get(self,url,timeout=5,proxy=None,num_retries=6):
    	print(u'开始获取：',url)
    	UA = random.choice(self.user_agents)
    	headers = {'User-Agent':UA}
    	if proxy == None:
    		try:
    			return requests.get(url,headers=headers,timeout=timeout)
    		except:
    			if num_retries > 0:
    				print('获取网页出错，10s后将获取倒数第：',num_retries,'次')
    				time.sleep(10)
    				return self.get(url,timeout,num_retries-1)
    			else:
    				print('开始使用代理')
    				time.sleep(10)
    				IP = ''.join(str(random.choice(self.iplist)).strip())
    				proxy = {'http':IP}
    				return self.get(url,time,proxy)
    	else:
    		try:
    			IP = ''.join(str(random.choice(self.iplist)).strip())
    			proxy = {'http':IP}
    			return requests.get(url,headers=headers,proxies=proxy,timeout=timeout)
    		except:
    			if num_retries > 0:
    				time.sleep(10)
    				IP = ''.join(str(random.choice(self.iplist)).strip())
    				proxy = {'http':IP}
    				print('当前代理是：',proxy)
    				return self.get(url,timeout,proxy,num_retries-1)
    			else:
    				print('代理也不好使了！取消代理')
    				return self.get(url)


request = download()




