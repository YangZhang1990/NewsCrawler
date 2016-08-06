import pyodbc
from newsItem import *


def insertRow(newsItem):
	try:
		conn = pyodbc.connect('DRIVER={SQL Server};SERVER=kapytest1.database.windows.net,1433', user='kapygroup', password='Kapykapy1234', database='databaseTest1')
		cursor=conn.cursor()

		# Prepare SQL query to INSERT a record into the database.

		sql ="INSERT INTO dbo.newsTestBBC(uniqueName,newsTitle,newsdate, newstime, source, origURL, description,category,author,picURL) VALUES (?,?,?,?,?,?,?,?,?,?)"

		try:
			# Execute the  SQL command
			#print news.title
			#print news.date
			#print news.category
			cursor.execute(sql,(newsItem.title,newsItem.complete_title,newsItem.date,newsItem.time,newsItem.source_name,newsItem.origin_url,newsItem.description,newsItem.category,newsItem.author,newsItem.pic_url))
			# Commit your changes in the database
			conn.commit()
			print 'success insert data'
		except:
			# Rollback in case there is any error
			conn.rollback()
			print "failed insert data"

		conn.close()
		#print 'insertion finish'

	except:
		print "connection failed2"
