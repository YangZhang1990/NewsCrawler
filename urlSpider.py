import urllib
import urllib2
import sys
from general import *
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from dataconnet import *
from newsItem import *

class urlSpider:
	# Class variables shared among all instances

	#project_name =''
	project_name=''
	base_url= ''
	domain_name = ''
	queue_file =''
	crawled_file =''
	crawled_item_file=''
	queue = set()
	crawled_url = set()
	crawled_item = set()

	def __init__(self,project_name,base_url,domain_name):
		urlSpider.project_name= project_name
		urlSpider.base_url= base_url
		urlSpider.domain_name = domain_name
		urlSpider.queue_file = urlSpider.project_name + '/queue.txt'
		urlSpider.crawled_file = urlSpider.project_name + '/crawled.txt'
		urlSpider.crawled_item_file = urlSpider.project_name + '/crawledItems.txt'
		self.boot()
		self.crawl_page_urls('First Spider',urlSpider.base_url)

	@staticmethod
	def boot():
		create_project_dir(urlSpider.project_name)
		create_data_files(urlSpider.project_name,urlSpider.base_url)
		urlSpider.queue = file_to_set(urlSpider.queue_file)
		urlSpider.crawled_url = file_to_set(urlSpider.crawled_file)
		urlSpider.crawled_item = file_to_set(urlSpider.crawled_item_file)

	@staticmethod
	def crawl_page_urls(thread_name, page_url):
		#while len(urlSpider.crawled)<=1000:
			if page_url not in urlSpider.crawled_url:
				#print(thread_name+ ' now crawling '+page_url)
				print('Queue: '+ str(len(urlSpider.queue)) + '| Crawled :'+str(len(urlSpider.crawled_item)))
				if len(urlSpider.crawled_item)<=5000:
					urlSpider.add_links_to_queue(urlSpider.find_links(page_url))
					urlSpider.queue.remove(page_url)
					urlSpider.crawled_url.add(page_url)
					
					news = urlSpider.find_PageItem(page_url)
					if news != None:
						urlSpider.crawled_item.add(page_url)
					else:
						print page_url
					urlSpider.update_files()
				else:
					print 'finished'
					sys.exit(0)
					#newsSpider('fox')

	@staticmethod
	def find_PageItem(page_url):
		try:                       
			r= requests.get(page_url)
			soup = BeautifulSoup(r.content,'lxml')
			complete_title = soup.find('h1',{'class':'story-body__h1'}).next
			title= complete_title.replace(' ','').replace("'","").replace('!','').replace(':','')[:49]
			#print title
            #<div class="date date--v2 relative-time" data-seconds="1470425392" data-datetime="5 August 2016" data-timestamp-inserted="true">6 hours ago</div>
			timestamp=soup.find('li',{'class':'mini-info-list__item'})
			date=timestamp.find('div',{'class':'date date--v2'}).next
			#print date
            #time= timestamp['data-seconds'][11:19]
			time=''
			#print time
			author=''
			try:
				author=soup.find('div',{'class':'byline'}).find('span',{'class':'byline__name'}).next[3:]
			except:
				pass
			#print author
			source_name='BBC News'
			try:
				source_name= soup.find('div',{'itemprop':'sourceOrganization'}).find('a').next
			except:
				pass
			#print source_name
			origin_url=page_url
			#print origin_url
			pic_url=''
			try:
				image=soup.find('img',{'class':'js-image-replace'})
				pic_url=image['src']
                #pic_info=soup.find('figcaption',{'class':'media-caption'})
				#print pic_url
			except:
				pass
			category_div=soup.find('div',{'class':'secondary-navigation secondary-navigation--wide'})
			category=category_div.find('a',{'class':'secondary-navigation__title navigation-wide-list__link '}).find('span').next
            #second_category = category_div.find('a',{'class':'navigation-wide-list__link navigation-wide-list__link--first navigation-wide-list__link--last"'}).find('span').next
            #print second_category
			#print category
			article_contents= soup.find('div',{'class':'story-body__inner'}).find_all('p')
			description=''
			for paragraph in article_contents:
				description=description+paragraph.text.replace("'",'')+'\n'
			#print description
			news = newsItem(title,complete_title,time,date,source_name,description,origin_url,category,author,pic_url)
			insertRow(news)
			return news
		except:
        	#pass
			#print page_url 
			print('skip this page')
			return None

	@staticmethod
	def find_links(base_url):
		try:
			r= requests.get(base_url)
			soup = BeautifulSoup(r.content,"lxml")
			original_links = soup.find_all('a')
			links=set()
			for link in original_links:
				full_url = urljoin(base_url,link.get('href'))
				#print full_url
				links.add(full_url)
		except:
			print('Error: can not crawl page')
			return set()
		return links

	@staticmethod
	def add_links_to_queue(links):
		for url in links:
			#print url
			if url in urlSpider.queue:
				continue
			if url in urlSpider.crawled_url:
				continue
			if urlSpider.domain_name not in url:
				continue

			'''
			if 'shop.foxnews' in url:
				#print url
				continue
			if 'live.foxnews' in url:
				#print url
				continue
			if 'careers.foxnews' in url:
				#print url
				continue
			if 'radio.foxnews' in url:
				#print url
				continue
			if 'help' in url:
				#print url
				continue
			if 'video.foxnews' in url:
				#print url
				continue
			if 'video.latino' in url:
				#print url
				continue
			if 'latino.foxnews' in url:
				#print url
				continue
			if 'nation.foxnews' in url:
				#print url
				continue
			if 'com/on-air' in url:
				#print url
				continue
			if 'print' in url:
				#print url
				continue
			'''
			urlSpider.queue.add(url)

	@staticmethod
	def update_files():
		set_to_file(urlSpider.queue,urlSpider.queue_file)
		set_to_file(urlSpider.crawled_url,urlSpider.crawled_file)
		set_to_file(urlSpider.crawled_item,urlSpider.crawled_item_file)

PROJECT_NAME = 'bbc'
HOMEPAGE = 'http://www.bbc.com/news'
DOMAIN_NAME = 'bbc.com'
urlSpider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME)

