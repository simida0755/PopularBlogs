from django.db import models
from users.models import UserProfile
from course.models import Course,Lesson

from datetime import datetime
# Create your models here.
class UserAsk(models.Model):
    name = models.CharField('姓名',max_length=20)
    mobile = models.CharField('手机',max_length=11)
    bug_url = models.CharField('bug网址',max_length=50)
    bug_desc = models.CharField('bug描述',max_length=150)
    add_time = models.DateTimeField('添加时间',default=datetime.now)

    class Meta:
        verbose_name = 'bug反馈'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class UserMessage(models.Model):
    user = models.IntegerField('接受用户',default=0)
    message = models.CharField('消息内容',max_length=500)
    has_read = models.BooleanField('是否已读',default=False)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,verbose_name='教程',on_delete=models.CASCADE)
    comments = models.CharField('评论',max_length=200)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '教程评论'
        verbose_name_plural = verbose_name

class LessonQuestion(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,verbose_name='章节',on_delete=models.CASCADE)
    questions = models.CharField('问题',max_length=200)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '章节问题'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,verbose_name='教程',on_delete=models.CASCADE)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    FAV_TYPE = (
        (1,'教程'),
        (2,'博客文章'),
        (3,'博主')
    )

    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    fav_id = models.IntegerField('数据id',default=0)
    fav_type = models.IntegerField(verbose_name='收藏类型',choices=FAV_TYPE,default=1)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

