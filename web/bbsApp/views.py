from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
# Create your views here.
# select * from table ;
# ORM -> modelName.objects.all() : 전체를 가져옴

# select * from table where id = xxxx ;
# ORM -> modelName.objects.get(id = xxxx) ; 조건을 만족하는 것만 가져옴
# ORM -> modelName.objects.filter(id = xxxx) ;

# select * from table where id = xxxx and pwd = xxxx ;
# ORM -> modelName.objects.get(id = xxxx, pwd = xxxx) ;

# select * from table where id = xxxx or pwd = xxxx ;
# ORM -> modelName.objects.filter(Q(id = xxxx)| Q(pwd = xxxx)) ;

# select * from table where subject like '%공지%'
# ORM -> modelName.objects.filter(subject_icontains='공지')

# select * from table where subject like '공지%'
# ORM -> modelName.objects.filter(subject_startswith='공지')

# select * from table where subject like '%공지'
# ORM -> modelName.objects.filter(subject_endswith='공지')

# insert into table values()
# model(attr=value,attr=value)
# model.save()

# delete * from tableName where id = xxxx
# ORM -> modelName.objects.get(id=xxx).delete()

# update tableName set attr=val where id=xxxx
# ORM -> obj=modelName.objects.get(id=xxx)
# obj.attr = value
# obj.save() -- commit



def index(request) :
    if request.session.get('user_id') and request.session.get('user_name') :
        context = {'id' : request.session['user_id'],
                   'name' : request.session['user_name']}
        return render(request,'home.html',context)
    else :
        return render(request, 'login.html')

def logout(request) :
    request.session['user_name'] = {}
    request.session['user_id'] = {}
    request.session.modified = True
    return redirect('index')

def loginProc(request) :
    print('request - loginProc')
    if request.method == 'GET' :
        return redirect('index')
    elif request.method == 'POST' :
        id = request.POST['id']
        pwd = request.POST['pwd']
        user = BbsUserRegister.objects.get(user_id=id,user_pwd=pwd)
        print('user result - ',  user)
        context = {}
        if user is not None :
            # session create
            request.session['user_name'] = user.user_name
            request.session['user_id'] = user.user_id
            # session write
            context['name'] = request.session['user_name']
            context['id'] = request.session['user_id']
            return render(request,'home.html',context)
        else :
            return redirect('index')

def registerForm(request) :
    print('request - registerForm')
    return render(request,'join.html')

def register(request) :
    if request.method == 'POST' :
        id = request.POST['id']
        pwd = request.POST['pwd']
        name = request.POST['name']
        register = BbsUserRegister(user_id=id,user_pwd=pwd,user_name=name)
        register.save()
    return render(request,'login.html')

def bbs_list(request) :
    # select * from bbs ;
    # modelName.objects.all()
    boards = Bbs.objects.all()
    print('bbs_list request - ', type(boards),boards)
    context = {'boards' : boards,
               'name' : request.session['user_name'],
               'id' : request.session['user_id']}
    return render(request, 'list.html',context)

def bbs_registerForm(request) :
    print('request bbs_registerForm - ')
    context = {'name' : request.session['user_name'],
               'id' : request.session['user_id']}
    return render(request, 'bbsRegisterForm.html',context)

def bbs_register(request) :
    title = request.POST['title']
    content = request.POST['content']
    writer = request.POST['writer']
    print('request bbs_register - ',title, content, writer)
    board = Bbs(title = title, content = content, writer = writer)
    board.save()
    return redirect('bbs_list')

# get 방식
def bbs_read(request, id) :
    print('request bbs_read param id - ', id)
    board = Bbs.objects.get(id=id)
    board.viewCnt = board.viewCnt + 1
    board.save()
    print('request bbs_read result - ', board)
    context = {'board' : board,
               'name': request.session['user_name'],
               'id': request.session['user_id']
               }
    return render(request, 'read.html',context)

def bbs_remove(request) :
    id = request.POST['id']
    print('request bbs_remove param id - ', id)
    Bbs.objects.get(id=id).delete()
    return redirect('bbs_list')

def bbs_modifyForm(request) :
    id = request.POST['id']
    print('request bbs_modifyForm param id - ', id)
    board = Bbs.objects.get(id=id)
    context = {'board': board,
               'name': request.session['user_name'],
               'id': request.session['user_id']
               }
    return render(request,'modify.html',context)

def bbs_modify(request) :
    id = request.POST['id']
    title = request.POST['title']
    content = request.POST['content']
    writer = request.POST['writer']
    print('request modify - ', id, title, content, writer)
    board = Bbs.objects.get(id=id)
    board.title = title
    board.content = content
    board.save()
    return redirect('bbs_list')

def bbs_search(request) :
    type = request.POST['type']
    keyword = request.POST['keyword']
    print('request bbs_search - ', type, keyword)
    if type == 'title' :
        boards = Bbs.objects.filter(title__icontains = keyword)
    if type == 'writer' :
        boards = Bbs.objects.filter(writer__startswith=keyword)
    list = []
    for board in boards :
        list.append({
            'id' : board.id,
            'title' : board.title,
            'writer' : board.writer,
            'regdate' : board.regdate,
            'viewcnt' : board.viewCnt
        })
    return JsonResponse(list, safe=False)
