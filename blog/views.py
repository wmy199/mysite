from django.shortcuts import render,get_object_or_404
from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from ReadStatistics.models import ReadNum,read_time_statistics
from comment.forms import CommentForm


def blog_list(request):
    page_num = request.GET.get('page',1) #获取页码参数（get请求 假如没有就默认为1）
    all_blogs = Blog.objects.all()
    paginator =  Paginator(all_blogs,10) #每10个为一页
    page =  paginator.get_page(page_num)
    current_page = page.number
    page_range = list(range(max(current_page-2,1),min(current_page+2,paginator.num_pages)+1))
    context = {}
    context['blogs'] = page
    context['blog_types']=BlogType.objects.all()
    context['page_range'] = page_range
    context['last_page'] = paginator.num_pages
    context['blog_dates'] = Blog.objects.dates('created_time','month',order='DESC')
    return render(request,'blog_list.html',context)



def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    key = read_time_statistics(request,blog)
    comments =  blog.comments.all()
    context['blog'] = get_object_or_404(Blog,pk=blog_pk)
    context['comments'] = comments

    context['comment_form'] = CommentForm(initial = {'content_type':blog.__class__.__name__.lower(),'object_id':blog.pk})
    response = render(request,'blog_detail.html',context)
    response.set_cookie('blog_%s_readed' % blog_pk,value='true',max_age=60)
    return response


def blogs_with_type(request,blogs_with_type):
    
    blog_type=get_object_or_404(BlogType,type_name=blogs_with_type)
    
    page_num = request.GET.get('page',1) #获取页码参数（get请求 假如没有就默认为1）
    all_blogs = Blog.objects.filter(blog_type=blog_type)
    paginator =  Paginator(all_blogs,10) #每10个为一页
    page = paginator.get_page(page_num)
    current_page = page.number
    page_range = list(range(max(current_page-2,1),min(current_page+2,paginator.num_pages)+1))
    context = {}
    context['blogs'] = page
    context['type'] = blog_type
    context['page_range'] = page_range
    context['blog_types']=BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time','month',order='DESC')
    return render(request,'blogs_with_type.html',context)

    
def blogs_with_date(request,year,month):
    page_num = request.GET.get('page',1)
    all_blogs = Blog.objects.filter(created_time__year=year,created_time__month=month)
    paginator =  Paginator(all_blogs,10) #每10个为一页
    page = paginator.get_page(page_num)
    current_page = page.number
    page_range = list(range(max(current_page-2,1),min(current_page+2,paginator.num_pages)+1))

    context = {}
    context['blog_date'] = "%s年%s月" % (year,month)
    context['blogs'] = page
    context['page_range'] = page_range
    context['blog_types']=BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time','month',order='DESC')
    return render(request,'blogs_with_date.html',context)
