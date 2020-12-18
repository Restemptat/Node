import requests
import bs4
import re
from datetime import datetime, timedelta
import csv

headings = [
    'politika', 'economika', 'obschestvo', 'mir', 'criminal',
    'technology', 'zdorovie', 'cultura', 'sport', 'pogoda'
]


def get_news(date: datetime, heading):
    date_str = date.strftime('%Y-%m-%d')
    response = requests.get(f"https://www.1tv.ru/news/{heading}/{date_str}")
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    data = soup.findAll(['article', 'div'], {"class": ["card itv-col-wrap", 'itv-col-wrap card date']})
    articles = []
    for element in data:
        if 'date' in element['class']:
            break
        else:
            articles.append(element)

    for article in articles:
        a_tag = article.find('a')
        href = a_tag.attrs['href']
        title = a_tag.find('div', {'class': 'title'})
        text = title.text
        text = re.sub(r"^\s*", "", text)
        text = re.sub(r"\s*$", "", text)
        text = re.sub(u'\xa0', ' ', text)
        yield href, text


if __name__ == '__main__':
    with open('news.csv', mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'url', 'rubric', 'date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames,  lineterminator='\n')
        writer.writeheader()
        date = datetime.today()
        for i in range(365):
            for heading in headings:
                rubric = heading.title()
                for news in get_news(date, heading):
                    href, text = news
                    writer.writerow({'title': text, 'url': href, 'rubric': rubric, 'date': date.strftime('%d.%m.%Y')})
            date -= timedelta(days=1)
