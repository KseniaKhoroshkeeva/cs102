import requests
from bs4 import BeautifulSoup
from time import sleep


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    item_list = parser.find('table', {'class': 'itemlist'})

    title_list = [i.text for i in item_list.find_all('a', {'class': 'storylink'})]
    url_list = [i['href'] for i in item_list.find_all('a', {'class': 'storylink'})]
    author_list = [i.text for i in item_list.find_all('a', {'class': 'hnuser'})]
    points_list = [int(''.join(s for s in i.text if s.isdigit())) for i in item_list.find_all('span', {'class': 'score'})]
    comments_list = []
    for i in item_list.find_all('td', {'class': 'subtext'}):
        temp = i.find_all('a')[-1].text
        if 'comment' in temp:
            comments_list.append(int(''.join(s for s in temp if s.isdigit())))
        else:
            comments_list.append(0)
    for i in range(len(author_list)):
        news_list.append({
            'author': author_list[i],
            'comments': comments_list[i],
            'points': points_list[i],
            'title': title_list[i],
            'url': url_list[i]})
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.find('a', {'class': 'morelink'})['href']


def get_news(url="https://news.ycombinator.com/", n_pages=1):
    """ Collect news from a given web page """
    news = []
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        if n_pages:
            sleep(5)
    return news

