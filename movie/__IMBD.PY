import requests
from bs4 import BeautifulSoup
import xlwt

class IMBD():
	def __init__(self):
		self.url_list = [
		'http://www.dytt8.net/html/gndy/jddy/20160320/50523.html',
    	'http://www.dytt8.net/html/gndy/jddy/20160320/50523_2.html',
    	'http://www.dytt8.net/html/gndy/jddy/20160320/50523_3.html',
    	'http://www.dytt8.net/html/gndy/jddy/20160320/50523_4.html'
		]
		self.msgs_list = []

	def save_xls(self,msg_list):
		'''创建 excel 文件'''
		book = xlwt.Workbook()
		row1 = 1
		print('储存 all_mssg_sheet ...')
		sheet = book.add_sheet('all_msg')
		sheet.write(0,0,'Name')
		sheet.write(0,1,'Score')
		sheet.write(0,2,'Year')
		sheet.write(0,3,'Href')
		for msg in msg_list: 
			sheet.write(row1,0,msg[0])
			sheet.write(row1,1,msg[1])
			sheet.write(row1,2,msg[2])
			sheet.write(row1,3,msg[3])
			row1 += 1
		print('完成!!!共读取',len(self.msgs_list),'条信息！！')
		book.save(r'IMBD.xls')


	def msgs_tool(self,msgs):
		'''对抓取到的 HTML 数据进行整理'''
		for i in msgs:
			if 'br' in str(i):
				try:
					text = i.get_text()
					score = text.split()[1]
					year = text.split()[2]
					name = text.split()[3]
					href = i.a['href']
					#print('Name:',name)
					#print('Score:',score)
					#print('Year:',year)
					#print('Url:',href)
					self.msgs_list.append((name,score,year,href))
				except:
					pass


	def get_msgs(self,url):
		'''开干'''
		html = requests.get(url)
		html.encoding = 'gb2312'
		soup = BeautifulSoup(html.text,'lxml')
		msgs = soup.find_all('p')
		self.msgs_tool(msgs)

	def begin(self):
		for url in self.url_list:
			self.get_msgs(url)

		self.save_xls(self.msgs_list)


if __name__ == '__main__':
	imbd = IMBD()
	imbd.begin()


