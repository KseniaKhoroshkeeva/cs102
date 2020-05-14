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


def fill_database(n_pages=10):
    s = session()
    news_list = get_news('https://news.ycombinator.com/newest', n_pages)
    for n in news_list:
        news = News(
            title=n['title'],
            author=n['author'],
            url=n['url'],
            comments=n['comments'],
            points=n['points']
        )
        s.add(news)
    s.commit()
