from django.shortcuts import render, redirect
from pytrends.request import TrendReq
from datetime import datetime, time, timedelta
import json
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
        list1 = word1
        pytrends.build_payload(list1, cat=0, timeframe= f'{date}', geo='', gprop='')
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
            k['link'] = '/anal'
            value_word1.append(k)
        dict1 = pytrends.related_queries()
        dict2 = dict1[f'{word1}']
        bubble_w1 = []
        for bbw in dict1:
            bbw1 = {}
            if len(dict1[f'{word1}']['top']['value'])>10:
                for n in range(0,10):
                    bbw1['text'] = dict1[f'{word1}']['top']['query'][n]
                    bbw1['count'] = dict1[f'{word1}']['top']['value'][n]
                bubble_w1.append(bbw1)
            else:
                for n in range(0, len(dict1[f'{word1}']['top']['value'])):
                    bbw1['text'] = dict1[f'{word1}']['top']['query'][n]
                    bbw1['count'] = dict1[f'{word1}']['top']['value'][n]
                bubble_w1.append(bbw1)
        context = {'vw1':value_word1, 'word1':word1, 'bw1':bubble_w1}
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
            k['link'] = '/anal'
            value_word1.append(k)
            z['label'] = h2
            z['y'] = a[2]
            z['link'] = '/anal'
            value_word2.append(z)
        dict1 = pytrends.related_queries()
        dict2 = dict1[f'{word1}']
        dict3 = dict1[f'{word2}']
        bubble_w1 = []
        bubble_w2 = []
        for bbw in dict1:
            bbw1 = {}
            bbw2 = {}
            if len(dict1[f'{word1}']['top']['value'])>10:
                for n in range(0,10):
                    bbw1['text'] = dict1[f'{word1}']['top']['query'][n]
                    bbw1['count'] = dict1[f'{word1}']['top']['value'][n]
                    bubble_w1.append(bbw1)
                if len(dict1[f'{word2}']['top']['value'])>10:
                    for n in range(0,10):
                        bbw2['text'] = dict1[f'{word2}']['top']['query'][n]
                        bbw2['count'] = dict1[f'{word2}']['top']['value'][n]
                    bubble_w2.append(bbw2)
                else:
                    for n in range(0, len(dict1[f'{word2}']['top']['value'])):
                        bbw2['text'] = dict1[f'{word2}']['top']['query'][n]
                        bbw2['count'] = dict1[f'{word2}']['top']['value'][n]
                    bubble_w2.append(bbw2)
            else:
                for n in range(0, len(dict1[f'{word1}']['top']['value'])):
                    bbw1['text'] = dict1[f'{word1}']['top']['query'][n]
                    bbw1['count'] = dict1[f'{word1}']['top']['value'][n]
                bubble_w1.append(bbw1)
                if len(dict1[f'{word2}']['top']['value'])>10:
                    for n in range(0,10):
                        bbw2['text'] = dict1[f'{word2}']['top']['query'][n]
                        bbw2['count'] = dict1[f'{word2}']['top']['value'][n]
                    bubble_w2.append(bbw2)
                else:
                    for n in range(0, len(dict1[f'{word2}']['top']['value'])):
                        bbw2['text'] = dict1[f'{word2}']['top']['query'][n]
                        bbw2['count'] = dict1[f'{word2}']['top']['value'][n]
                    bubble_w2.append(bbw2)
        context = {'vw1':value_word1, 'vw2':value_word2, 'word1':word1, 'word2':word2, 'bw1':bubble_w1, 'bw2':bubble_w2}
        return render(request, 'tot/graph.html', context)



    
