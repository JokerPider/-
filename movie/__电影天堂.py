from selenium import webdriver
import re
import time

class DYTT():

	def __init__(self):
		self.url = 'http://www.dy2018.com/7/'
		self.page = 1
		self.msg_list = []
		self.browser = webdriver.PhantomJS()

	def get_time(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))


	def get_list(self,html):
		item_list = []
		p = re.compile('评分:(.*?)<.*?片名:(.*?)◎',re.S)
		items = re.findall(p,html)
		for item in items:
			name = item[1].strip()
			score = item[0].strip()
			item_list.append((score,name))
		return item_list


	def begin(self,url):
		self.browser.get(url)
		print(self.get_time(),'开始第 %s 页,共 104 页...' % self.page)
		html = self.browser.page_source
		self.msg_list += self.get_list(html)
		self.page += 1
		if self.page <= 104:
			url = self.url + 'index_' + str(self.page) + '.html'
			self.begin(url)
		return self.msg_list

if __name__ == '__main__':
	url = 'http://www.dy2018.com/7/'
	dytt = DYTT()
	msg_list = dytt.begin(url)
	
	msg_list = list(set(msg_list))
	msg_list.sort()
	msg_list.reverse()
	
	n = 0
	for i in msg_list:
		n += 1
		print(i)
	print('共 ',n,' 部电影','惊悚片')

	


