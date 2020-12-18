import requests
import re


if __name__ == '__main__':
    response = requests.get('https://www.kommersant.ru/archive/rubric/4/month/2020-10-01')
    result = re.findall(r'<h3 class="article_name">(.*[Кк]оронавирус.*)<\/h3>', response.text)
    for i, line in enumerate(result):
        print(f"{i + 1}. {line}")