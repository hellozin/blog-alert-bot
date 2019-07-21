import os
import requests
import slackPostman as sp
from bs4 import BeautifulSoup

line_career_url = 'https://recruit.linepluscorp.com/lineplus/career/list?classId=148'
base_url = 'https://recruit.linepluscorp.com/'

def get_stored_seqs():
  seqs = []
  if os.path.isfile('line.txt'):
    file = open('line.txt', 'r', -1, 'utf-8')
    lines = file.readlines()
    for line in lines:
      tokens = line.split()
      seq = tokens[0]
      seqs.append(seq)
  return seqs

def save_new_recruits(new_recruits):
  file = open('line.txt', 'a', -1, 'utf-8')
  for recruit in new_recruits:
    file.write(recruit + '\n')

def send_updates(new_recruits):
  if len(new_recruits) > 0:
    message = '새 공고가 올라왔습니다.'
    for recruit in new_recruits:
      message = message + '\n' + recruit
    sp.send(message)

def recruit_tostring(seq, link, title, level, due):
  return seq+' '+level+' '+title+' '+due+' '+base_url+link

line_html = requests.get(line_career_url).text

soup = BeautifulSoup(line_html, 'html.parser')
table = soup.select('body > div.container > div.jobs_wrap > table > tbody > tr')

print(get_stored_seqs())

new_recruits = []
for tr in table:
  td = tr.find_all('td')
  seq = td[0].text
  link = td[1].find('a').get('href')
  title = td[1].find('a').text
  level = td[3].text
  due = td[4].text
  if seq not in get_stored_seqs():
    new_recruits.append(recruit_tostring(seq,link,title,level,due))

save_new_recruits(new_recruits)
send_updates(new_recruits)