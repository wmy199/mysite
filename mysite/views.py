from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.db.models import Sum
from django.utils import timezone
import datetime
from ReadStatistics.models import ReadLog
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
def seven_days_readtimes(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
                       #表示一天的时间
        readlogs =  ReadLog.objects.filter(content_type=content_type,date=date)
        
        
        result = readlogs.aggregate(readtimes=Sum('read_num'))
        #聚合    返回readlogs(QuerySet)中read_num的和 结果为字典{'readtimes':和}

        read_nums.append(result['readtimes'] or 0)
    return dates,read_nums 

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_logs = ReadLog.objects.filter(date=today,content_type=content_type).order_by('-read_num')
    return  read_logs[0:5]

def get_seven_days_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_logs = Blog.objects.filter(read_logs__date__lt=today,read_logs__date__gte=date) \
                .values('pk','title') \
                .annotate(read_num = Sum('read_logs__read_num')) \
                .order_by('-read_num')
   
    return read_logs[:5]




def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = seven_days_readtimes(blog_content_type)

    today_hot_datas = get_today_hot_data(blog_content_type)

    seven_days_hot_datas = cache.get('seven_days_hot_datas')
    if seven_days_hot_datas is None:
        seven_days_hot_datas = get_seven_days_hot_data(blog_content_type)
        cache.set('seven_days_hot_datas',seven_days_hot_datas,3600*24)
    else:
        print('caches')

    
    context['today_hot_datas'] = today_hot_datas
    context['seven_days_hot_datas'] = seven_days_hot_datas
    context['read_nums'] = read_nums
    context['dates'] = dates
    return render(request,'home.html',context)

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    page = request.POST.get('page',reverse('home'))
    
    user = auth.authenticate(request,username=username,password=password)
    

    #网址重定向 
    if user is not None:
        auth.login(request,user)
        return redirect(page)
    else:
        return render(request,'error.html',{'message':'用户名或密码不正确'})

def goto_login_page(request):


    page =  request.GET.get('from','')
    return render(request,'login.html',{'page':page})