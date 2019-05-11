from django.db import models

# Create your models here.
from datetime import datetime


class BlogOrg(models.Model):

    ORG_CHOICES = (
        ("bkpt", u"博客平台"),
        ("gr", u"个人"),
    )

    # 添加字段

    category = models.CharField(max_length=20, choices=ORG_CHOICES, verbose_name=u"博客类别", default="gr")

    name = models.CharField('平台名称',max_length=50)
    desc = models.TextField('平台描述')
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    image = models.ImageField('封面图',upload_to='org/%Y%m',max_length=100)
    address = models.CharField('机构域名',max_length=150,)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '博客平台'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blogger(models.Model):
    org = models.ForeignKey(BlogOrg,verbose_name='所属平台',on_delete=models.CASCADE)
    name = models.CharField('博主名',max_length=50)
    blog_url = models.CharField('博客地址',max_length=50,default= '')

    work_years = models.IntegerField('工作年限',default=0)
    work_company = models.CharField('就职公司',max_length=50)
    work_position = models.CharField('公司职位',max_length=50)
    points = models.CharField('博客特点',max_length=50)
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    add_time = models.DateTimeField(default=datetime.now)
    image = models.ImageField(
        default='image/default.png',
        upload_to="blogger/%Y/%m",
        verbose_name="头像",
        max_length=100)

    class Meta:
        verbose_name = '博主'
        verbose_name_plural = verbose_name

    def get_category(self):
        return self.org.category

    def get_course_nums(self):
        return self.course_set.count()

    def get_posts_nums(self):
        return self.blogposts_set.count()

    def __str__(self):
        return "[{0}]的博主: {1}".format(self.org, self.name)