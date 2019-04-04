from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone





# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id =models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

class ReadLog(models.Model):
    date = models.DateTimeField(default = timezone.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id =models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

def read_time_statistics(request,obj):
    type = ContentType.objects.get_for_model(obj)
    key = '%s_%s_readed' % (type.model,obj.pk)
    if not request.COOKIES.get(key):
        # 如果存在阅读次数（ReadNum）的话就次数加1，没有就创建并加1（创建ReadNum默认值为0）       
        readnum = ReadNum.objects.filter(content_type=type,object_id=obj.pk)     
        if readnum:
            readnum = readnum[0]
        else:
            readnum = ReadNum(content_type=type,object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        
        date = timezone.now().date()
        readlog = ReadLog.objects.filter(content_type = type,object_id=obj.pk,date=date)
        if readlog:
            readlog = readlog[0]      
        else:
            readlog = ReadLog(content_type=type,object_id=obj.pk,date=date)

        #可以改成  readlog,created = ReadLog.objects.get_or_create(content_type = Type,object_id = obj,date=date)
        #如果找到了符合条件的对象就返回为readlog，created为false
        #没找到就创建一个对象并返回为readlon，created为true       上面的ReadNum也可以用

        readlog.read_num += 1
        readlog.save()
    return key

