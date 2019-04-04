from django.urls import path
from . import views

urlpatterns =[
    path('',views.blog_list,name='blog_home'),
    path('<int:blog_pk>',views.blog_detail,name="blog_detail"),
    path('type/<str:blogs_with_type>',views.blogs_with_type,name='blogs_with_type'),
    path('date/<int:year>/<int:month>',views.blogs_with_date,name='blogs_with_date'),
    
]