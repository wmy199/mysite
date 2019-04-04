from django.shortcuts import render,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse
# Create your views here.



def update_comment(request):
    user = request.user
    referer = request.META.get('HTTP_REFERER',reversed('home'))
    comment_form = CommentForm(request.POST,user = user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
    else:
        data = {}
        data['status'] = 'ERROR'
        

    return JsonResponse(data)
    