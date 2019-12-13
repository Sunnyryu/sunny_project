# -*- coding: utf-8 -*-
#googlefuncs.py

import urllib.request
import requests
import re
from bs4 import BeautifulSoup
import time
import random
from urllib.request import urlopen
import re


#--------------------------------------------------------------------------
# cnt개의 뉴스 제목과 링크 반환
#--------------------------------------------------------------------------
def get_newslist(search_words, cnt, datebf7, date):
    encText = urllib.parse.quote(search_words)
    baseUrl = 'https://www.google.co.kr/search?q='
    dayUrl = "&tbs=cdr%3A1%2Ccd_min%3A"+datebf7[4:6]+"%2F"+datebf7[6:8]+"%2F"+datebf7[0:4]+"%2Ccd_max%3A"+date[4:6]+"%2F"+date[6:8]+"%2F"+date[0:4]
    suffix1 = "&tbm=nws&start="
    suffix2 = "&sa=N"
    # header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    #     (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    p = re.compile(r"\?q=.*&sa")

    newsList = []
    start = 0
    while len(newsList) < cnt:
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0")]
            html = opener.open(baseUrl + encText + dayUrl + suffix1 + str(start) + suffix2)
            # res = requests.get(
            #     baseUrl + encText + dayUrl + suffix1 + str(start) + suffix2)

            #블럭 당하면 caller 에게 -1로 알림
            soup =  BeautifulSoup(html.read(), 'html.parser')
            # if re.compile(r"Our systems have detected").search(html.text):
            #     return -1 

            # candList = soup.select('#ires ol div table h3 a')
            title = []
            link = []
            items  = soup.findAll("h3")
            if len(items) == 0: break   # 뉴스가 모자라면 그만둠
            for item in items:
                itemA = item.a
                title.append(itemA)
                link.append(itemA['href'])
        
            for list1, list2 in zip(title, link):
                if len(newsList) >= cnt: break # 뉴스를 다 채우면 중단
                print("google: " + list1.text, list2)
                newsList.append({"title" : list1.text, "link" : list2})
            # for cand in candList:
            #     if len(newsList) >= cnt: break # 다 채웠으면 그만둠
            #     m = p.search(cand.get('href'))
            #     if m:
            #         link = m.group()[3:-3]
            #         newsList.append({
            #             'title' : cand.text,
            #             'link' : urllib.parse.unquote(link).strip() })
            #     else:
            #           print("skipped: " + itemA.get('href'))
        except Exception as e:
            print(e)
        finally:
            start += 10 # 다음 페이지
            wait = round(random.uniform(0, 2.5), 1)
            print("random sleep {} sec...".format(wait))
            time.sleep(wait)

    return newsList


#--------------------------------------------------------------------------
# module test code - getNewsList()
#--------------------------------------------------------------------------
if __name__ == "__main__":
    newsList = get_newslist("삼성", 20,"20190210","20190211") # 뉴스 11개 테스트
    for news in newsList: print(news['title'], news['link'])
