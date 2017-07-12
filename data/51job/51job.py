import requests
import xlwt
from bs4 import BeautifulSoup
import random
import time 
from multiprocessing import Process

class QCWY():
	def __init__(self,begin):
		self.msg_list = []
		#self.useless_url = []
		#self.useless_page = []
		self.begin = begin
		self.UA_list = [
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", 
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", 
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", 
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", 
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", 
"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", 
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", 
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", 
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
		]
		#self.jtype_list = []
		#self.education_list = []
		#self.experience_list = []
		#self.pay_list = []
		#self.ctype0_list = []
		#self.ctype1_list = []
		#self.ctype2_list = []


	def get_time(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))


	#def page_list(self):
	#	page_list = []
	#	for page in range(self.begin,2001,5):
	#		url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=030200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keywordtype=2&curr_page='+str(page)+'&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confirmdate=9'
	#		page_list.append(url)
	#	page_list.reverse()
	#	return page_list


	def page_list(self):
		page_list = ['http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=030200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=Python&keywordtype=2&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&dibiaoid=0&confirmdate=9']
		return page_list

	def get_one_page_href(self,url):
		html = requests.get(url)
		html.encoding = 'gbk'
		soup = BeautifulSoup(html.text,'lxml')
		page_url = soup.find('div',class_='dw_table',id='resultList').find_all('p',class_='t1')
		url_list = []
		for i in page_url:
			url_list.append(i.find('a',target='_blank')['href'])
		return url_list

	def get(self,url):
		UA = random.choice(self.UA_list)
		headers = {'User-Agent':UA}
		html = requests.get(url,headers=headers)
		html.encoding = 'gb2312'
		return html.text

	def get_one_msg(self,url):
		try:
			html = self.get(url)
			soup = BeautifulSoup(html,'lxml')
			main0 = soup.find('div',class_='cn')
			jname = main0.h1['title']
			jtypes = soup.find('p',class_='fp f2').find_all('span',class_='el')
			jtype = []
			for i in jtypes:
				jtype.append(i.get_text())
			jtype = '\\'.join(jtype)
			pay_text = main0.strong.get_text() ## '1-2千/月'  '1-2万/月'  '10万-20万/年'
			pay = pay_text[:-3]
			if '万' in pay_text and '年' not in pay_text:
				pay = str(int(float(pay_text[:-3].split('-')[0])*10)) + '-' + str(int(float(pay_text[:-3].split('-')[1])*10))
			address = main0.span.get_text()
			cname = main0.p.a.get_text()
			ctype = main0.find_all('p')[1].get_text().split('|')  
			c0 = ctype[0].strip()  #公司性质
			c1 = ctype[1].strip()  #公司规模
			c2 = (ctype[2].strip() if len(ctype) == 3 else None)  #公司类型
			
			main1 = soup.find('div',class_='t1')
			i1 = i2 = i3 = i4 = i5 = i6 = None
			spans = main1.find_all('span')
			for span in spans:
				if 'i1' in str(span):
					i1 = span.get_text()
				elif 'i2' in str(span):
					i2 = span.get_text()
				elif 'i3' in str(span):
					try:
						i3 = int(span.get_text()[2:-1])
					except:
						i3 = span.get_text()[2:-1]
				elif 'i4' in str(span):
					i4 = span.get_text()
				elif 'i5' in str(span):
					i5 = span.get_text()
				elif 'i6' in str(span):
					i6 = span.get_text()

			# i1 --> 经验 # i2 --> 学历 # i3 --> 招聘人数 # i4 --> 发布时间 # i5 --> 语言 # i6 ——> 专业
			#main2 = soup.find('p',class_='t2')	# 福利
			#if str(main2) != 'None':
			#	main2 = main2.get_text().split()
			#	main2 = '/'.join(main2)

			#self.education_list.append(i2)
			#self.experience_list.append(i1)
			#self.pay_list.append(pay)
			#self.ctype0_list.append(c0)
			#self.ctype1_list.append(c1)
			#self.ctype1_list.append(c2)
			self.msg_list.append([jname,pay,jtype,address,i2,i1,cname,c0,c1,c2,i3,i5,i6,url])
		except:
			print('\n无法读取的网址：%s \n'%url)
			#self.useless_url.append(url)


	def get_one_page_msg(self,href):
		n = 1
		for url in href:
			try:
				print('|'*n,'.'*(49-n))
				self.get_one_msg(url)
				n += 1
			except:
				print(self.get_time(),'第 %s 条无法读取...'%n)
				#self.useless_url.append(url)

	def save_msg(self,msg_list):
		book = xlwt.Workbook()

		sheet1 = book.add_sheet('招聘信息')
		n = 0
		for item in ('职位','薪酬k/月','类型','地点','学历','经验','公司','性质','规模','类型','人数','语言','专业','更多'):
			sheet1.write(0,n,item)
			n += 1
		row1 = 1
		for msg in msg_list:
			col1 = 0
			for i in msg:
				sheet1.write(row1,col1,i)
				col1 += 1
			row1 += 1

		#sheet2 = book.add_sheet('无效网址')
		#row2 = 0
		#for usel in self.useless_url:
		#	sheet2.write(row2,0,usel)
		#	row2 += 1

		#sheet2.write(row2+1,0,'开始时间：')
		#sheet2.write(row2+1,2,self.begin_time)
		#sheet2.write(row2 + 2,0,'结束时间：')
		#sheet2.write(row2 + 2,2,self.get_time())

		#count1 = '共采集'+ str(len(self.msg_list)) + '有效条信息' 
		#sheet2.write(row2+4,0,count1)
		#count2 = str(len(self.useless_url)) +'条网址无法读取'
		#count3 = str(len(self.useless_page))+ '个目录页面无法读取'
		#sheet2.write(row2+5,0,count2)
		#sheet2.write(row2+6,0,count3)

		sheet3 = book.add_sheet('统计')

		sheet3.write(0,0,'职位')
		sheet3.write(0,1,'count')
		row3 = 1
		jtype_list = []
		for jt in self.msg_list:
			num = jt[-4]
			jt = jt[2].split('\\')
			if isinstance(num,int):
				jt *= num
			for j in jt:
				jtype_list.append(j)
		for ty in set(jtype_list):
			num = jtype_list.count(ty)
			sheet3.write(row3,0,ty)
			sheet3.write(row3,1,num)
			row3 += 1

		sheet3.write(0,2,'薪酬')
		sheet3.write(0,3,'count')
		row6 = 1
		pay_list = []
		for pa in self.msg_list:
			pay_list.append(pa[1])
		for ty in set(pay_list):
			num = pay_list.count(ty)
			sheet3.write(row6,2,ty)
			sheet3.write(row6,3,num)
			row6 += 1


		sheet3.write(0,4,'学历')
		sheet3.write(0,5,'count')
		row4 = 1
		education_list = []
		for ed in self.msg_list:
			education_list.append(ed[4])
		for ty in set(education_list):
			num = education_list.count(ty)
			sheet3.write(row4,4,ty)
			sheet3.write(row4,5,num)
			row4 += 1

		sheet3.write(0,6,'经验')
		sheet3.write(0,7,'count')
		row5 = 1
		experience_list = []
		for ex in self.msg_list:
			experience_list.append(ex[5])
		for ty in set(experience_list):
			num = experience_list.count(ty)
			sheet3.write(row5,6,ty)
			sheet3.write(row5,7,num)
			row5 += 1


		sheet3.write(0,8,'性质')
		sheet3.write(0,9,'count')
		row7 = 1
		ctype0_list = []
		for ct0 in self.msg_list:
			ctype0_list.append(ct0[7])
		for ty in set(ctype0_list):
			num = ctype0_list.count(ty)
			sheet3.write(row7,8,ty)
			sheet3.write(row7,9,num)
			row7 += 1

		sheet3.write(0,10,'规模')
		sheet3.write(0,11,'count')
		row8 = 1
		ctype1_list = []
		for ct1 in self.msg_list:
			ctype1_list.append(ct1[8])
		for ty in set(ctype1_list):
			num = ctype1_list.count(ty)
			sheet3.write(row8,10,ty)
			sheet3.write(row8,11,num)
			row8 += 1

		sheet3.write(0,12,'公司类型')
		sheet3.write(0,13,'count')
		row9 = 1
		ctype2_list = []
		for ct2 in self.msg_list:
			if ct2[9] != None :
				ctype2_list += ct2[9].split(',')
			else:
				ctype2_list.append(ct2[9])
		for ty in set(ctype2_list):
			num = ctype2_list.count(ty)
			sheet3.write(row9,12,ty)
			sheet3.write(row9,13,num)
			row9 += 1

		sheet3.write(0,14,'语言')
		sheet3.write(0,15,'count')
		row10 = 1
		lan_list = []
		for la in self.msg_list:
			lan_list.append(la[11])
		for ty in set(lan_list):
			num = lan_list.count(ty)
			sheet3.write(row10,14,ty)
			sheet3.write(row10,15,num)
			row10 += 1

		book_name = str(time.strftime('[%Y%m%d %H-%M-%S]',time.localtime(time.time()))) + '.xls'
		book.save(book_name)


	def main(self):
		self.begin_time = self.get_time()
		all_page = self.page_list()
		n = 1
		for url in all_page:
			try:	
				print('\n开始读取第 %s 页\n'%n)
				n+=1
				one_page_href = self.get_one_page_href(url)
				self.get_one_page_msg(one_page_href)
			except:
				print('\n第 %s 页无法读取？？？？？？\n'%n)
				self.useless_page.append(url)
		self.save_msg(self.msg_list)


if __name__ == '__main__':

	#for i in range(1,6):
	#	q = QCWY(i)
	#	p = Process(target=q.main)
	#	p.start()

	q = QCWY(1)
	q.main()


