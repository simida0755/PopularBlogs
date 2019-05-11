from datetime import datetime

from django.db import models
from organization.models import Blogger
from DjangoUeditor.models import UEditorField

class Course(models.Model):
    DEGREE_CHOICES = (
        ("py", "python"),
        ("ja", "java"),
        ("C", "C++"),
        ("zw","杂文"),
    )
    NANDU_CHOICES = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )

    name = models.CharField("教程名",max_length=50)
    desc = models.CharField("教程描述",max_length=300)
    # detail = models.TextField("课程详情")
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    category = models.CharField("文章分类", choices=DEGREE_CHOICES, max_length=2,null=True,)
    nandu = models.CharField("难度", choices=NANDU_CHOICES, max_length=2,null=True,)
    tag = models.CharField('课程标签', default='', max_length=10)
    blogger = models.ForeignKey(Blogger,verbose_name='所属博主',null=True,on_delete=models.CASCADE)
    is_banner = models.BooleanField('是否轮播',default=False)
    students = models.IntegerField("学习人数",default=0)
    Like_nums = models.IntegerField("点赞人数",default=0)
    fav_nums = models.IntegerField("收藏人数",default=0)
    image = models.ImageField("封面图",upload_to="courses/%Y/%m",max_length=100,)
    click_nums = models.IntegerField("点击数",default=0)
    add_time = models.DateTimeField("添加时间",default=datetime.now,)
    youneed_know = models.CharField('课程须知',max_length=300,default='')
    teacher_tell = models.CharField('老师告诉你',max_length=300,default='')


    class Meta:
        verbose_name = "教程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_nums(self):
        return self.lesson_set.count()

    def get_course_lesson(self):
        return self.lesson_set.all()

class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name='教程',on_delete=models.CASCADE)
    name = models.CharField("章节名",max_length=100)
    add_time = models.DateTimeField("添加时间",default=datetime.now)
    lesson_url = models.CharField("章节网址",max_length=100,default='',null=False)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》教程的章节 >> {1}'.format(self.course, self.name)

    def go_url(self):
        from django.utils.safestring import mark_safe
        import requests
        # mark_safe后就不会转义
        try:
            html_old = requests.get(self.lesson_url)
            html_buffer = html_old.text.split('<div id="cnblogs_post_body" class="blogpost-body">')
            html_new = html_buffer[1].split('<div id="MySignature">')[0]
            return mark_safe(html_new)
        except:
            format = "<a href='%s'>解析源地址出错，建议自行跳转</a>"
            return mark_safe(format % self.lesson_url)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="教程",on_delete=models.CASCADE)
    name = models.CharField("名称",max_length=100)
    download = models.FileField("资源文件",upload_to="course/resource/%Y/%m",max_length=100)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "教程资源"
        verbose_name_plural = verbose_name


class BlogPosts(models.Model):
    DEGREE_CHOICES = (
        ("py", "python"),
        ("ja", "java"),
        ("C", "C++"),
        ("zw","杂文"),
    )

    name = models.CharField("博客文章名",max_length=50)
    desc = models.CharField("文章描述",max_length=300,null=True,blank=True)
    detail = models.TextField("文章详情")
    blog_url = models.CharField('网址',max_length=100,default='',null=False)
    blogger = models.ForeignKey(Blogger,verbose_name='所属博主',null=True,blank=True,on_delete=models.CASCADE)
    category = models.CharField("文章分类",choices=DEGREE_CHOICES,max_length=2,null=True)
    like_nums = models.IntegerField("点赞人数",default=0)
    fav_nums = models.IntegerField("收藏人数",default=0)
    click_nums = models.IntegerField("点击数",default=0)
    add_time = models.DateTimeField("添加时间",default=datetime.now,)

    class Meta:
        verbose_name = "博客文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def go_url(self):
        from django.utils.safestring import mark_safe
        import requests
        # mark_safe后就不会转义
        try:
            html_old = requests.get(self.blog_url)
            html_buffer = html_old.text.split('<div id="cnblogs_post_body" class="blogpost-body">')
            html_new = html_buffer[1].split('<div id="MySignature">')[0]
            return mark_safe(html_new)
        except:
            format = "<a href='%s'>解析源地址出错，建议自行跳转</a>"
            return mark_safe(format % self.blog_url)


