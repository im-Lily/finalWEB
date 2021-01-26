from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def index(request) :
    print('request index - ')
    return render(request, 'frontDemo.html')

def nonAjax(request) :
    print('request ajax - nonAjax')
    list = [{'id': 'multicampus04', 'pwd': 'multicampus04'},
            {'id': 'multicampus05', 'pwd': 'multicampus05'}]
    # safe = False -> 비동기통신
    return JsonResponse(list,safe=False)

def paramAjax(request) :
    id = request.POST['user_id']
    pwd = request.POST['user_pwd']
    print('ajax param - ', id, pwd)
    list = [{'id': 'multicampus04', 'pwd': 'multicampus04'},
            {'id': 'multicampus05', 'pwd': 'multicampus05'}]
    # safe = False -> 비동기통신
    return JsonResponse(list, safe=False)

def chart(request) :
    return render(request, 'chartDemo.html')

