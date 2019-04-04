from django.contrib import admin
from .models import ReadNum,ReadLog
# Register your models here.

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_type','object_id')

@admin.register(ReadLog)
class ReadLogAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_type','object_id','date')