from bs4 import BeautifulSoup
import random
import xlwt
import time
from heiheihei.proxy import request_with_proxy
from heiheihei.Download import request

class ZPH:
	def __init__(self):
		self.msg_list = []
		self.useless_url = []

	def get_soup(self,url):
		print(1)
		html = request_with_proxy.get(url)
		html.encoding = 'utf-8'
		soup = BeautifulSoup(html.text,'lxml')
		return soup

	def get2_soup(self,url):
		print(2)
		html = request.get(url)
		soup = BeautifulSoup(html.text,'lxml')
		return soup

	def get_page(self,work_url):
		print(3)
		page_list = []
		soup = self.get_soup(work_url)
		all_page = soup.find('div',id = 'fanye').find_all('a')
		for page in all_page:
			page = 'http://gzbys.job168.com:8080/companyOfTheMeetingListWeb.action' + page['href']
			page_list.append(page)
		return page_list

	def get_url(self,page):
		print(4)
		url_list = []
		soup = self.get_soup(page)
		all_a = soup.find_all('a',target='_blank')
		for a in all_a:
			url = 'http://gzbys.job168.com:8080' + a['href']
			url_list.append(url)
		return url_list

	def get_url_list(self,page_list):
		print(5)
		url_list = []
		for page in page_list:
			each_page_list = self.get_url(page)
			url_list += each_page_list
		return url_list

	def save_msg(self,url_list):
		print(6)
		x = 1
		y = len(url_list)
		for url in url_list:
			print(x,'/',y)
			x += 1
			try:
				soup = self.get2_soup(url)
				cname = soup.find('div',class_='company').b.get_text()
				ctype1 = soup.find('div',class_='company').get_text().split()[1][5:]
				ctype2 = soup.find('div',class_='company').get_text().split()[2][5:]
				jname = soup.find('div',class_='boxpos').p.get_text()[:-5].strip()
				jnum = int(soup.find('div',class_='boxpos').p.get_text()[-5:].strip().strip('(').strip(')').strip('人'))
				if jnum == '公司简介':
					continue
				five_msg = []
				all_p = soup.find('div',class_='poscontent').find_all('p')
				for p in all_p:
					msg = p.get_text().split('：')[1].strip()
					five_msg.append(msg)
				one_job_msg = [cname,ctype1,ctype2,jname,jnum] + five_msg[1:] + [url]
				self.msg_list.append(one_job_msg)
			except:
				self.useless_url.append(url)

	def save(self,msg_list):
		print(7)
		book = xlwt.Workbook()
		sheet = book.add_sheet('message')
		n = 0
		for item in ['conpanyName','conpanyNature','conpanyType','jobName','number','education','major','name','other','money','more']:
			sheet.write(0,n,item)
			n += 1
		row = 1
		for msg in self.msg_list:
			col = 0
			for i in msg:
				sheet.write(row,col,i)
				col += 1
			row += 1

		sheet1 = book.add_sheet('无法读取的信息')
		row1 = 0
		for useless_url in self.useless_url:
			sheet1.write(row1,0,useless_url)
			row1 += 1

		book.save('哈哈哈'+self.file_name+'.xls')

	def begin(self,work_url):
		print(8)
		self.file_name = work_url.split('=')[1]
		page_list = self.get_page(work_url)
		url_list = self.get_url_list(page_list)
		self.save_msg(url_list)
		self.save(self.msg_list)

if __name__ == '__main__':
	from config import work_list
	zph = ZPH()
	for url in work_list:
		zph.begin(url)