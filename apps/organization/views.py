from django.shortcuts import render

from django.views.generic import View
from organization.models import Blogger,BlogOrg
from course.models import Course,BlogPosts
from operation.models import UserFavorite
from pure_pagination import Paginator,PageNotAnInteger
from django.http import HttpResponse
from .forms import UserAskForm
from django.db.models import Q
# Create your views here.
class BloggerListView(View):
    '''博主列表'''
    def get(self,request):
        all_blogger = Blogger.objects.all()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # icontains是包含的意思（不区分大小写）
            # Q可以实现多个字段，之间是or的关系
            all_blogger = all_blogger.filter(
                Q(name__icontains=search_keywords) | Q(blog_url__contains=search_keywords))
        #有多少位博主
        blogger_nums = all_blogger.count()
        sort = request.GET.get('sort', "")
        category = request.GET.get('ct','')
        if category:
            all_blogger = all_blogger.filter(org__category=category)
        if sort:
            if sort == "fav_nums":
                all_blogger = all_blogger.order_by("-fav_nums")
            elif sort == "click_nums":
                all_blogger = all_blogger.order_by("-click_nums")

        hot_org = BlogOrg.objects.all().order_by('-click_nums')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_blogger, 5, request=request)
        blogers = p.page(page)


        return render(request,'blogger-list.html',{
            'all_blogger':blogers,
            'blogger_nums':blogger_nums,
            "category": category,
            'sort': sort,
            'hot_org':hot_org
        })




class AddUserAskView(View):
    """
    用户bug反馈
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的数据类型
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class BloggerHomeView(View):
    '''博主首页'''
    def get(self,request,blogger_id):
        current_page = 'home'
        # 根据id找到课程机构
        blogger = Blogger.objects.get(id = int(blogger_id))
        blogger.click_nums += 1
        blogger.save()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=blogger.id, fav_type=3):
                has_fav = True
        all_posts = blogger.blogposts_set.all()[:2]
        all_courses = blogger.course_set.all()[:2]
        return render(request, 'blogger-detail-homepage.html',{
            'all_posts': all_posts,
            'all_courses': all_courses,
            'blogger': blogger,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class BloggerDescView(View):
    '''博主介绍'''

    def get(self, request, blogger_id):
        current_page = 'desc'
        # 根据id找到课程机构
        blogger = Blogger.objects.get(id=int(blogger_id))
        blogger.click_nums += 1
        blogger.save()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=blogger.id, fav_type=3):
                has_fav = True
        return render(request, 'blogger-detail-desc.html', {
            'blogger': blogger,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class BloggerPostsView(View):
    '''博主文章'''

    def get(self, request, blogger_id):
        current_page = 'posts'
        # 根据id找到课程机构
        blogger = Blogger.objects.get(id=int(blogger_id))
        blogger.click_nums += 1
        blogger.save()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=blogger.id, fav_type=3):
                has_fav = True
        all_posts = blogger.blogposts_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示2个
        p = Paginator(all_posts, 2, request=request)
        posts = p.page(page)
        return render(request, 'blogger-detail-posts.html', {
            'all_posts': posts,
            'blogger': blogger,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class BloggerCourseView(View):
    '''博主教程'''

    def get(self, request, blogger_id):
        current_page = 'course'
        # 根据id找到课程机构
        blogger = Blogger.objects.get(id=int(blogger_id))
        blogger.click_nums += 1
        blogger.save()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=blogger.id, fav_type=3):
                has_fav = True
        all_courses = blogger.course_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示2个
        p = Paginator(all_courses, 2, request=request)
        courses = p.page(page)

        return render(request, 'blogger-detail-course.html', {
            'all_courses': courses,
            'blogger': blogger,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self, request):
        id = request.POST.get('fav_id', 0)         # 防止后边int(fav_id)时出错
        type = request.POST.get('fav_type', 0)     # 防止int(fav_type)出错

        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_record:
            # 如果记录已经存在，表示用户取消收藏
            exist_record.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                blogposts = BlogPosts.objects.get(id=int(id))
                blogposts.fav_nums -= 1
                if blogposts.fav_nums < 0:
                    blogposts.fav_nums = 0
                blogposts.save()
            elif int(type) == 3:
                blogger = Blogger.objects.get(id=int(id))
                blogger.fav_nums -= 1
                if blogger.fav_nums < 0:
                    blogger.fav_nums = 0
                blogger.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    blogposts = BlogPosts.objects.get(id=int(id))
                    blogposts.fav_nums += 1
                    blogposts.save()
                elif int(type) == 3:
                    blogger = Blogger.objects.get(id=int(id))
                    blogger.fav_nums += 1
                    blogger.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')