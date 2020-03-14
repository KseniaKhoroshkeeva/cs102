from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import get_news

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)

def news1000(n=34):
    all_pages = get_news(n_pages=n)
    s = session()
    for i in range(len(all_pages)):
        news = News(title = all_pages[i]['title'],
        author=all_pages[i]['author'],
        url=all_pages[i]['url'],
        comments=all_pages[i]['comments'],
        points=all_pages[i]['points'])
        s.add(news)
    s.commit()

news1000(n=1)