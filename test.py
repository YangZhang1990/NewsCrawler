import urllib
import urllib2
import sys
from general import *
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from dataconnet import *
from newsItem import *
def find_PageItem(page_url):
                              
            r= requests.get(page_url)
            soup = BeautifulSoup(r.content,'lxml')
            complete_title = soup.find('h1',{'class':'story-body__h1'}).next
            title= complete_title.replace(' ','').replace("'","").replace('!','').replace(':','')[:49]
            #print title
            #<div class="date date--v2 relative-time" data-seconds="1470425392" data-datetime="5 August 2016" data-timestamp-inserted="true">6 hours ago</div>
            try:
                timestamp=soup.find('li',{'class':'mini-info-list__item'})
                date=timestamp.find('div',{'class':'date date--v2'}).next
            except:
                pass
            try:
                date=soup.find('p',{'class':'date date--v1'})
            except:
                pass
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
            try:
                article_contents= soup.find('div',{'class':'story-body__inner'}).find_all('p')
                description=''
                for paragraph in article_contents:
                    description=description+paragraph.text.replace("'",'')+'\n'
            except:
                pass
            try:
                article_contents= soup.find('div',{'class':'map-body'}).find_all('p')
                description=''
                for paragraph in article_contents:
                    description=description+paragraph.text.replace("'",'')+'\n'
            except:
                pass
            #print description
            news = newsItem(title,complete_title,time,date,source_name,description,origin_url,category,author,pic_url)
            insertRow(news)
            return news

find_PageItem('http://www.bbc.com/news/world-middle-east-36278132')