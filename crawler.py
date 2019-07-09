import os
import requests
import hashlib
import slackPostman as sp
from bs4 import BeautifulSoup

def get_urls():
    r = requests.get('https://github.com/hellozin/blog-alert-bot/blob/master/README.md')
    html = r.text

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.select('p > a')

    urls = list(map(lambda a: a.get_text(),body))
    return urls

def get_today_contents(urls):
    today_contents = {}
    for url in urls:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        body = soup.select('body')
        text = body[0].get_text().replace('\n', '')
        hashVal = hashlib.sha256(text.encode('utf-8')).hexdigest()
        today_contents[url] = hashVal
    return today_contents

def get_old_contents(file):
    old_contents = {}
    lines = file.readlines()
    for line in lines:
        tokens = line.split()
        old_contents[tokens[0]] = tokens[1]
    return old_contents

urls = get_urls()
today_contents = get_today_contents(urls)

if os.path.isfile('contents.txt'):
    file = open('contents.txt', 'r')
    old_contents = get_old_contents(file)

    for url in urls:
        if url not in old_contents:
            sp.send(url + ' 이 알림 목록에 새로 추가되었습니다.')
        elif today_contents[url] != old_contents[url]:
            sp.send(url + ' 이 업데이트 되었습니다.')
            
    file.close()

file = open('contents.txt', 'w')
for url in urls:
    file.write(url + ' ' + today_contents[url])
    file.write('\n')
file.close()
print('end')
