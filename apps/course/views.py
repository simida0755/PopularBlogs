from django.shortcuts import render
from django.http import HttpResponse
from organization.models import BlogOrg
from operation.models import CourseComments,UserCourse,UserFavorite
from .models import BlogPosts,Course,CourseResource,Lesson
from pure_pagination import Paginator,PageNotAnInteger
from  django.views.generic import View
from django.db.models import Q
# Create your views here.


class PostsView(View):
    '''博文列表'''

    def get(self,request):
        #所有的博文
        all_posts = BlogPosts.objects.all()
        #所有博文的分类
        all_category = Course.DEGREE_CHOICES
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # icontains是包含的意思（不区分大小写）
            # Q可以实现多个字段，之间是or的关系
            all_posts = all_posts.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

        posts_nums = all_posts.count()
        sort = request.GET.get('sort', "")
        category = request.GET.get('lg','')
        if category:
            all_posts = all_posts.filter(category=category)
        if sort:
            if sort == "fav_nums":
                all_posts = all_posts.order_by("-fav_nums")
            elif sort == "click_nums":
                all_posts = all_posts.order_by("-click_nums")

        hot_org = BlogOrg.objects.all().order_by('-click_nums')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_posts, 5, request=request)
        posts = p.page(page)


        return render(request,'posts-list.html',{
            'all_posts':posts,
            'all_category':all_category,
            'posts_nums':posts_nums,
            "category": category,
            'sort': sort,
            'hot_org':hot_org
        })


class CourseView(View):
    '''教程列表'''

    def get(self,request):
        #所有的教程
        all_course = Course.objects.all()
        #所有教程的分类
        all_category = Course.DEGREE_CHOICES
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # icontains是包含的意思（不区分大小写）
            # Q可以实现多个字段，之间是or的关系
            all_course = all_course.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

        course_nums = all_course.count()
        sort = request.GET.get('sort', "")
        category = request.GET.get('lg','')
        if category:
            all_course = all_course.filter(category=category)
        if sort:
            if sort == "fav_nums":
                all_course = all_course.order_by("-fav_nums")
            elif sort == "click_nums":
                all_course = all_course.order_by("-click_nums")

        hot_org = BlogOrg.objects.all().order_by('-click_nums')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allcourse中取五个出来，每页显示5个
        p = Paginator(all_course, 5, request=request)
        course = p.page(page)


        return render(request,'course-list.html',{
            'all_course':course,
            'all_category':all_category,
            'course_nums':course_nums,
            "category": category,
            'sort': sort,
            'hot_org':hot_org
        })

class CourseDetailView(View):
    '''教程详情页'''
    def get(self,request,course_id):

        course = Course.objects.get(id = int(course_id))
        # 课程的点击数加1
        course.click_nums += 1
        course.save()
        blogger = course.blogger
        has_fav_course = False
        has_fav_blogger = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.blogger.id, fav_type=3):
                has_fav_blogger = True
        tag = course.tag
        if tag:
            # 需要从1开始不然会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []

        return render(request,'course-detail.html',{
            'course':course,
            'blogger':blogger,
            "relate_courses":relate_courses,
            'has_fav_blogger':has_fav_blogger,
            'has_fav_course':has_fav_course,
        })

class CourseInfoView(View):
    '''课程章节页'''

    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            # 如果没有学习该门课程就关联起来
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
        # 相关课程推荐
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        user_ids_count = len(user_ids)
        # 通过所有用户的id,找到所有用户学习过的所有教程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        # 资源
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-info.html', {
            'course': course,
            'user_ids_count':user_ids_count,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })

class LessonInfoView(View):
    '''章节详情页'''

    def get(self,request,lesson_id):
        lesson = Lesson.objects.get(id=int(lesson_id))
        input_html = lesson.go_url()
        course = Course.objects.get(id=int(lesson.course.id))
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            # 如果没有学习该门课程就关联起来
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
        # 相关课程推荐
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        user_ids_count = len(user_ids)
        # 通过所有用户的id,找到所有用户学习过的所有教程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        # 资源
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'lesson-info.html', {
            'input_html':input_html,
            'course': course,
            'user_ids_count':user_ids_count,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })


class PostsInfoView(View):
    '''章节详情页'''

    def get(self,request,posts_id):
        posts = BlogPosts.objects.get(id=int(posts_id))
        blogger = posts.blogger
        input_html = posts.go_url()
        category = posts.get_category_display()
        relate_posts = BlogPosts.objects.filter(category= category).order_by("-like_nums")[:5]

        return render(request, 'posts-info.html', {
            'posts':posts,
            'blogger':blogger,
            'input_html':input_html,
            'relate_posts': relate_posts,
        })



class CommentsView(View):
    '''课程评论'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 取出所有课程id
        # 通过所有用户的id,找到所有用户学习过的所有教程
        # 找到学习这门课的所有用户的id
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        user_ids_count = len(user_ids)
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)

        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            'user_ids_count':user_ids_count,
            'relate_courses':relate_courses,
            "all_resources": all_resources,
            'all_comments':all_comments,
        })




#添加评论
class AddCommentsView(View):
    '''用户评论'''
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            # 实例化一个course_comments对象
            course_comments = CourseComments()
            # 获取评论的是哪门课程
            course = Course.objects.get(id = int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')
