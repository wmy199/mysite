from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions
from ReadStatistics.models import ReadNum,ReadLog
from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation

from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Read:
    def read_num(self):
        try:
            type = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=type,object_id = self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist as identifier:
            return 0

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model,Read):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    read_logs = GenericRelation(ReadLog)
    comments = GenericRelation(Comment)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
