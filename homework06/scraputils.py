import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    all_comments = []

    all_authors = [t.text for t in parser.find_all('a', class_ = 'hnuser')]
    all_points = [t.text for t in parser.find_all('span', class_ = 'score')]
    all_title = [t.text for t in parser.find_all('a', class_ = 'storylink')]
    all_url= [t['href'] for t in parser.find_all('a', class_ = 'storylink')]

    find_id = [t['id'] for t in parser.find_all('tr', class_= 'athing')]

    for i in range(len(find_id)):
        comments = [t.text for t in parser.find_all('a', {'href' : 'item?id='+ find_id[i]})]
        our_comment = str(comments[-1])
        if our_comment.find('comment') != -1:
            c = our_comment.find('c') - 1
            all_comments.append(int(our_comment[:c]))
        else:
            all_comments.append(0)    
    #print(len(all_points),len(all_title),len(all_url),len(all_authors),len(all_comments))
    d = {}
    for i in range(len(all_authors)):
        d = {'author': all_authors[i], 'comments': all_comments[i], 'points':all_points[i], 'title': all_title[i], 'url': all_url[i]}
        news_list.append(d)
    #print(news_list)


    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next_p = parser.find('a', class_ = 'morelink')['href']
    return next_p


def get_news(url="https://news.ycombinator.com/newest", n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        #print(next_page)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

