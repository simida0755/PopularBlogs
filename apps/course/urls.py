# organization/urls.py

from course.views import PostsView,CourseView,CourseDetailView,CourseInfoView,CommentsView,AddCommentsView,LessonInfoView,PostsInfoView

from django.urls import path,re_path

# 要写上app的名字
app_name = "course"

urlpatterns = [
    path('posts_list/',PostsView.as_view(),name='posts_list'),
    path('list/',CourseView.as_view(),name='course_list'),
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    # 课程章节信息页
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    re_path('lesson/(?P<lesson_id>\d+)/', LessonInfoView.as_view(), name="lesson"),
    re_path('posts/(?P<posts_id>\d+)/', PostsInfoView.as_view(), name="posts_info"),
    #课程评论
    re_path('comment/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"),
    #添加评论
    path('add_comment/', AddCommentsView.as_view(), name="add_comment"),
]