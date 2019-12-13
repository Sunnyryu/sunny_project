from django.shortcuts import render, redirect
from pytrends.request import TrendReq
from datetime import datetime, time, timedelta
from .harvesta import harvesta
from .preproca import preproca
import json
import requests
import sys
import subprocess
import os
import DateTime
# Create your views here.
def index(request):
    
    return render(request, 'tot/index.html') 

def graph(request):
    words = request.GET.get('q')
    if not words:
        return redirect('tot:index')
    date = request.GET.get('y')
    a = ','
    pytrends = TrendReq()
    #pytrends = TrendReq(hl='ko', tz=540)
    if a not in words:
        if request.GET.get('y')=='year':
            date = 'today 12-m'
        elif request.GET.get('y')=='month':
            date = 'today 1-m'
        else:
            date = 'now 7-d'
        word1 = words
        list1 = [word1]
        pytrends.build_payload(list1, cat=0, timeframe= f'{date}', geo='', gprop='')
        #pytrends.build_payload(list1, cat=0, timeframe= f'{date}', geo='', gprop='youtube')
        value = pytrends.interest_over_time()
        del value['isPartial']
        value = value.reset_index()
        value2 = value.to_json(force_ascii=False, orient='split', date_format='iso', date_unit='s')
        value_dict = json.loads(value2)
        value_word1 = []
        for a in value_dict['data']:
            k = {}
            h = datetime.strptime(a[0],'%Y-%m-%dT%H:%M:%SZ')
            h2 = h.strftime('%Y-%m-%d %H:%M:%S')
            k['label'] = h2
            k['y'] = a[1]
            #k['link'] = '/anal'
            value_word1.append(k)
        dict1 = pytrends.related_queries()
        dict2 = dict1[f'{word1}']
        newdict1 = {}
        if len(dict2['top']['value']) > 10:
            newdict1 = dict2['top'][0:10]
            newdict1 = newdict1.to_dict()
        else:
            newdict1 = dict2['top']
            newdict1 = newdict1.to_dict()
        context = {'vw1':value_word1, 'word1':word1, 'newdict1': newdict1, 'date':date}
        return render(request, 'tot/graph.html', context)
    elif a in words:
        pass
        words = words.split(',')
        word1 = words[0]
        word2 = words[1]
        if request.GET.get('y')== 'year':
            date = 'today 12-m'
        elif request.GET.get('y') == 'month':
            date = 'today 1-m'
        else:
            date = 'now 7-d'
        list1 = [word1, word2]
        pytrends.build_payload(list1, cat=0, timeframe= f'{date}', geo='', gprop='')
        value = pytrends.interest_over_time()
        del value['isPartial']
        value = value.reset_index()
        value2 = value.to_json(force_ascii=False, orient='split', date_format='iso', date_unit='s')
        value_dict = json.loads(value2)
        value_word1 = []
        value_word2 = []
        for a in value_dict['data']:
            k = {}
            z = {}
            h = datetime.strptime(a[0],'%Y-%m-%dT%H:%M:%SZ')
            h2 = h.strftime('%Y-%m-%d %H:%M:%S')
            k['label'] = h2
            k['y'] = a[1]
            #k['link'] = '/anal'
            value_word1.append(k)
            z['label'] = h2
            z['y'] = a[2]
            #z['link'] = '/anal'
            value_word2.append(z)
        dict1 = pytrends.related_queries()
        dict2 = dict1[f'{word1}']
        dict3 = dict1[f'{word2}']
        newdict1 = {}
        newdict2 = {}
        if len(dict2['top']['value']) > 10:
            newdict1 = dict2['top'][0:10]
            newdict1 = newdict1.to_dict()
        else:
            newdict1 = dict2['top']
            newdict1 = newdict1.to_dict()
        if len(dict3['top']['value']) > 10:
            newdict2 = dict3['top'][0:10]
            newdict2 = newdict2.to_dict()
        else:
            newdict2 = dict3['top']
            newdict2 = newdict2.to_dict()

        
        context = {'vw1':value_word1, 'vw2':value_word2, 'word1':word1, 'word2':word2, 'newdict2':newdict2, 'newdict1':newdict1, 'date':date}
        return render(request, 'tot/graph.html', context)

def search(request):
    if request.GET.get('word2'):
        word1 = request.GET.get('word1')
        word2 = request.GET.get('word2')
        word3 = request.GET.get('cd')
        date = request.GET.get('date')
        list1 = [word1, word2]
        pytrends = TrendReq(hl='ko', tz=540)
        pytrends.build_payload(list1, cat=0, timeframe= f'{date}', geo='', gprop='youtube')
        dict1 = pytrends.related_queries()
        dict2= dict1[f'{word3}']
        bubble = []
        if len(dict2['top']['value'])>10:
            for n in range(0,10):
                bbw1 = {}
                bbw1['text'] = dict2['top']['query'][n]
                bbw1['count'] = dict2['top']['value'][n]
                bubble.append(bbw1)
        else:
            for n in range(0, len(dict2['top']['value'])):
                bbw1 = {}
                bbw1['text'] = dict2['top']['query'][n]
                bbw1['count'] = dict2['top']['value'][n]
                bubble.append(bbw1)
        context = {'bubble':bubble, 'date':date}
        
        return render(request, 'tot/search.html', context)
    else:
        word1 = request.GET.get('word1')
        word3 = request.GET.get('cd')
        date = request.GET.get('date')
        list1 = [word1]
        pytrends = TrendReq()
        pytrends.build_payload(list1, cat=0, timeframe= f'{date}', geo='', gprop='youtube')
        dict1 = pytrends.related_queries()
        dict2= dict1[f'{word3}']
        bubble = []
        
        if len(dict2['top']['value'])>10:
            for n in range(0,10):
                bbw1 = {}
                bbw1['text'] = dict2['top']['query'][n]
                bbw1['count'] = dict2['top']['value'][n]
                bubble.append(bbw1)
        else:
            for n in range(0, len(dict2['top']['value'])):
                bbw1 = {}
                bbw1['text'] = dict2['top']['query'][n]
                bbw1['count'] = dict2['top']['value'][n]
                bubble.append(bbw1)
        context = {'bubble':bubble, 'date':date}
        return render(request, 'tot/search.html', context)

def youtube(request):
    date = request.GET.get('date')
    text = request.GET.get('text')
    print(date)
    print(text)
    return render(request, 'tot/youtube.html')    

def anal(request):
    date = request.GET.get('date')
    keyword = request.GET.get('keyword')
    datebf7 = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    datebf8 = datebf7 + timedelta(days=-7)
    datebf8 = datebf8.strftime('%Y%m%d %H:%M:%S')
    date = datebf7.strftime('%Y%m%d %H:%M:%S')
    date = date[0:8]
    print(date)
    datebf7 = datebf8[0:8]
    startpath ='./'
    print(datebf7)
    print(keyword)
    keyword_source_dic = {'ENTERPRISE':[keyword]}
    outPath = harvesta.harvest(startpath, datebf7, date, keyword_source_dic)
    preproca.preproc(outPath)
    #p = subprocess.Popen(['./tot/analyzas/analyza.py',outPath])
    #p.wait()
    current_time = datetime.today().strftime("%Y%m%d%H%M%S")
    current_ymd = current_time[2:8]
    current_time0 = current_time[8:10]+'00'
    #current_time1 = current_time +timedelta(hour=-1)
    #print(current_time1)

    print(os.path.isdir(f'/home/sunny/ubuntu/Project/Final_Project/Devel1/{current_ymd}/{current_time0}/'))
    print(os.path.dirname(os.path.realpath(__file__)) )
    directory =f'/home/sunny/ubuntu/Project/Final_Project/Devel1/{current_ymd}/{current_time0}/E_K_01/'
    outfile_name = "text.txt"
    out_file = open(f'{directory}/outfile_name', 'w')
    files= os.listdir(directory)
    if os.path.isdir(f'/home/sunny/ubuntu/Project/Final_Project/Devel1/{current_ymd}/{current_time0}/'):
        for filename in files:
            if ".txt" not in filename:
                continue
            file = open(directory + filename)
            for line in file:
                out_file.write(line)
            out_file.write("\n")
            file.close()
        out_file.close()
        
    else:
        pass
    txtfile = open(f'/home/sunny/ubuntu/Project/Final_Project/Devel1/{current_ymd}/{current_time0}/text.txt', 'r')
    print(txtfile)


    return render(request, 'tot/anal.html')

