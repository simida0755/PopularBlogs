# course/adminx.py

import xadmin

from .models import Course, Lesson, CourseResource,BlogPosts


class CourseAdmin(object):
    '''课程'''

    list_display = ['name', 'desc', 'detail', 'blogger','students']
    search_fields = ['name', 'desc', 'detail', 'blogger', 'students']
    list_filter = ['name', 'desc', 'detail', 'blogger', 'students']
    style_fields = {"detail": "ueditor"}

class LessonAdmin(object):
    '''章节'''

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # 这里course__name是根据教程名称过滤
    list_filter = ['course__name', 'name', 'add_time']



class CourseResourceAdmin(object):
    '''教程资源'''

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']

class BlogPostsAdmin(object):
    '''课程'''

    list_display = ['name', 'desc', 'detail', 'blogger','add_time']
    search_fields = ['name', 'desc', 'detail', 'blogger', 'add_time']
    list_filter = ['name', 'desc', 'detail', 'blogger', 'add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(BlogPosts, BlogPostsAdmin)