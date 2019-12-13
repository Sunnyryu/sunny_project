# -*- coding: utf-8 -*-
#naverFuncs.py

import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import json
if __name__ != '__main__':
    from . import config


#--------------------------------------------------------------------------
# 실시간 인기 검색어 cnt개 반환
#--------------------------------------------------------------------------
# def get_keywords(cnt):
#     naverUrl = "https://www.naver.com"
#     try:
#         html = requests.get(naverUrl, timeout=10).content
#         soup = BeautifulSoup(html, 'html.parser')
#         tagList = soup.select('.ah_roll_area .ah_k')
#         naver_keywords = []
#         for keyword in tagList:
#             naver_keywords.append(keyword.get_text())
#     except Exception as e:
#         print(e)
#         return naver_keywords
#     else:
#         #cnt 개의 결과만을 반환
#         return naver_keywords[:min([len(naver_keywords), cnt])]


#--------------------------------------------------------------------------
# 검색어로 뉴스를 검색하여 cnt개 반환
#--------------------------------------------------------------------------
# def get_newslist(search_words, cnt):
#     encText = urllib.parse.quote(search_words)
#     url = "".join(["https://openapi.naver.com/v1/search/news.json?",
#             "query={0}&display={1}&sort={2}"]).format(encText, cnt, "date") 

#     # NAVER API를 이용하여 검색
#     request = urllib.request.Request(url)
#     request.add_header("X-Naver-Client-Id", config.clientID)
#     request.add_header("X-Naver-Client-Secret", config.clientSecret)
#     try:
#         response = urllib.request.urlopen(request)
#     except Exception as e:
#         print(e)
#     else:
#         rescode = response.getcode()
#         if(rescode == 200):
#             response_body = response.read()
#             newsList = json.loads(response_body.decode('utf-8'))['items']

#             # title과 link만 추출하여 담기
#             resultList = []
#             for news in newsList:
#                 resultList.append({ 
#                     'title' : re.sub("<[^>]*>", '', news['title']),
#                     # 'link' : news['originallink'] != 
#                     #     '' and news['originallink'] or news['link']})
#                     'link' : news['link']})
#         else:
#             print("Error Code:" + rescode)
   
#     #결과 반환 (없으면 없는대로)
#     return resultList
def get_newslist(search_words, cnt, datebf7, date):
    
 
    # 네이버의 날짜 필터 형식은 YYYY.MM.DD

    encText = urllib.parse.quote(search_words)
    furl = "https://search.naver.com/search.naver?where=news&query="
    surl = "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds="+datebf7[0:4]+"."+datebf7[4:6]+"."+datebf7[6:8]+"&de="+date[0:4]+"."+date[4:6]+"."+date[6:8]
    lurl = "&docid=&nso=so:r,p:from"+datebf7+"to"+date+",a:all&mynews=0&refresh_start=0&start="
    # print(lurl)

    newsList = []
    oldLast = "I'm Old"
    i = 1
    while len(newsList) < cnt: # cnt개 채울 때 까지
        try:
            res = requests.get(furl + encText + surl + lurl + str(i))
            soup = BeautifulSoup(res.content, 'html.parser')
            urlname = soup.select("._sp_each_title")
            urllink = soup.select("a[class*=_sp_each_title]")
            urllink = [ re.sub(r"\?f=o", "", url.get('href')) 
                    for url in urllink ]
            # 뉴스가 모자라면 그만 둠
            if len(urlname) == 0: 
                break 

            # 같은 뉴스면 그만 둠
            currentLast = urllink[len(urllink)-1]
            if currentLast == oldLast: 
                break 
            oldLast = currentLast
            
            for list1, list2 in zip(urlname, urllink):
                if len(newsList) >= cnt: break # 뉴스를 다 채우면 중단
                print("naver: " + list1.text, list2)
                newsList.append({"title" : list1.text, "link" : list2})
            i += 10 # 다음 페이지
        except Exception as e:
            print(e)     
    return newsList


#--------------------------------------------------------------------------
# module test code
#--------------------------------------------------------------------------
if __name__ == "__main__":
    # naverKeywords = get_keywords(120)
    # print(naverKeywords)
    import config
    newsList = get_newslist("삼성중공업", 30,"20190210","20190211") #1 키워드 1 뉴스 테스트
    for news in newsList: print(news['title'], news['link'])
