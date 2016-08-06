class newsItem:
    newsID=''
    title=''
    time=''
    date=''
    description=''
    source_name=''
    author=''
    pic_url=''
    origin_url=''
    category=''

    def __init__(self, title,complete_title,time,date,source_name,description,origin_url,category,author,pic_url):
        self.title = title
        self.complete_title=complete_title
        self.date=date
        self.time=time
        self.description=description
        self.source_name=source_name
        self.origin_url=origin_url
        self.category=category  # instance variable unique to each instance
        self.author=author
        self.pic_url=pic_url
