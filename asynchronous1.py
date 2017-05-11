import tornado.ioloop
import bs4 as bs
import urllib.request
import requests
from bs4 import BeautifulSoup
import json
from TwitterSearch import *
from tornado.httpclient import AsyncHTTPClient

print('Enter Query:')
query1 = input()
query = str(query1)
urls = ['https://www.google.co.in/search?q={}'.format(query1),'http://api.duckduckgo.com/?q={}&format=json&pretty=1'.format(query1),'http://www.twitter.com/search?q={}'.format(query1)]

def handle_response(response):
    if response.error:
        print("Error:", response.error)
    else:
        url = response.request.url
        print(url)
        if url.find('google')!=-1:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            nextlink=soup.find('cite').text
            openurl = urllib.request.urlopen(nextlink).read()
            soup1 = bs.BeautifulSoup(openurl,'html.parser')
            paragraph=soup1.find('p')
            print({'Google':paragraph.text})

        elif url.find('duckduckgo')!=-1:
            response = requests.get(url).text
            response = json.loads(response)
            url1 = response['AbstractURL']
            result = requests.get(url1).text
            soup2 = bs.BeautifulSoup(result,'html.parser')
            print({'duckduckgo':soup2.title})
            'print(result)'
        elif url.find('twitter')!=-1:
            try:
                tso=TwitterSearchOrder()
                tso.set_keywords(['Modi','Kohli'])
                tso.set_language('en')
                tso.set_include_entities(False)
    
                ts = TwitterSearch(
                    consumer_key = 'DgHQosGZxyCj4v3YBou3juxI8',
                    consumer_secret = 'DJ4KBzpwhHw581CwNYY2wAiFC11jWbo7A1F86WLUFkSvNgdPPm',
                    access_token = '838303233361788928-6Rguis2fXQWMMa6fojnSyapem1WBWx7',
                    access_token_secret = 'MYhA3VGmaZlUrmUqaSJlLKja5VjszV4rXAdLSRN8J1nSg'
                )
                url3 = requests.get(url)
                soup = bs.BeautifulSoup(url3.text, "html.parser")

                for paragraph in soup.find_all('p'):
                    if(paragraph.find(query)):
                        print({'twitter':paragraph.text})
                        break

            except TwitterSearchException as e:
                print(e)

http_client = AsyncHTTPClient()
for url in urls:
    http_client.fetch(url, handle_response)
    
tornado.ioloop.IOLoop.instance().start()
