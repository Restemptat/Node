import sys
import requests
import json
import re
import tqdm
import time
 
 
class GitHubUser:
    def __init__(self, github_url):
        self.language = {}
        result = re.findall(r'^\s*http[s]?://github\.com/([a-zA-Z0-9]+)[/]?\s*$', github_url)
        if result:
            username = result[0]
            self.username = username
            response = requests.get(f"https://api.github.com/users/{username}/repos?")
            self.repos = response.json().copy()
 
            # response = requests.get(f"https://api.github.com/users/{username}/followers")
            # data = response.json()
            # print(type(data), len(data))
 
            response = requests.get(f"https://github.com/{username}")
            count = re.findall(r'<span class="text-bold text-gray-dark" >(\S+)</span>\s*followers', response.text)[0]
            count = count.replace('k', '000')
            self.followers_count = int(count)
        else:
            self.repos = []
            self.username = None
 
    def print_repos(self):
        for i, repo in enumerate(self.repos):
            print(f'{i + 1}. {repo["name"]}\nDescription: {repo["description"]}')
 
    def count_languages(self):
        # languages = {'C': 12, 'Python': 200}
        languages = {}
        for repo in self.repos:
            language = repo['language']
            if language:
                if language in languages:
                    languages[language] += 1
                else:
                    languages[language] = 1
        return languages
 
    def print_languages(self):
        languages = self.count_languages()
        print(f'List of languages: {", ".join(languages.keys())}')
        for language, count in languages.items():
            print(f'{language} - {count}')
 
 
def info_about_user(github_accounts, users):
    for i, github_account in enumerate(github_accounts):
        print(f'{i + 1}. {github_account}')
    while True:
        input_string = input('Enter the number: ')
        if input_string.isdigit():
            number = int(input_string)
            if 1 <= number <= len(github_accounts):
                users[number - 1].print_repos()
                break
            else:
                print(f'Please enter a number from {1} to {len(github_accounts)}')
        else:
            print('Only numbers can be entered!')
 
 
def user_languages(github_accounts, users):
    for i, github_account in enumerate(github_accounts):
        print(f'{i + 1}. {github_account}')
    while True:
        input_string = input('Enter the number: ')
        if input_string.isdigit():
            number = int(input_string)
            if 1 <= number <= len(github_accounts):
                users[number - 1].print_languages()
                break
            else:
                print(f'Please enter a number from {1} to {len(github_accounts)}')
        else:
            print('Only numbers can be entered!')
 
 
if __name__ == '__main__':
    github_accounts = sys.argv[1:]
 
    users = []
    for github_account in tqdm.tqdm(github_accounts):
        user = GitHubUser(github_account)
        users.append(user)
        time.sleep(0.5)
    while True:
        print('\nMAIN MENU')
        print('1 - user info, 2 - user languages')
        print('3 - repos count, 4 - most popular language')
        print('5 - followers amount')
        print('exit - to exit the program')
        event = input('Enter the command: ')
        if event == '1':
            info_about_user(github_accounts, users)
        elif event == '2':
            user_languages(github_accounts, users)
        elif event == '3':
            arr = sorted(users, key=lambda github_user: len(github_user.repos), reverse=True)
            print(f">> The largest number of repositories has: {arr[0].repos[0]['owner']['login']}")
        elif event == '4':
            languages = {}
            for github_user in users:
                for language, count in github_user.count_languages().items():
                    if language in languages.keys():
                        languages[language] += count
                    else:
                        languages[language] = count
            print(languages)
            most_popular_language = sorted(languages.keys(), key=lambda key: languages[key], reverse=True)[0]
            print(f">> The most popular language: {most_popular_language}")
        elif event == '5':
            sorted_users = sorted(users, key=lambda some_user: some_user.followers_count, reverse=True)
            print(f">> The user with the highest number of followers: {sorted_users[0].username}")
        elif event == 'exit':
            break
        else:
            print('>> Please enter 1, 2, 3 or exit')
