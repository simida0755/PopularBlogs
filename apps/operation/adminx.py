# operation/adminx.py

import xadmin

from .models import UserAsk, UserCourse, UserMessage, CourseComments, UserFavorite,LessonQuestion


class UserAskAdmin(object):
    '''BUG反馈表'''

    list_display = ['name', 'mobile', 'bug_url','bug_desc', 'add_time']
    search_fields = ['name', 'mobile', 'bug_url','bug_desc','course_name']
    list_filter = ['name', 'mobile', 'bug_url','bug_desc', 'add_time']


#
class UserCourseAdmin(object):
    '''用户教程学习'''

    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']



class UserMessageAdmin(object):
    '''用户消息后台'''

    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']



class CourseCommentsAdmin(object):
    '''用户评论后台'''

    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


class LessonQuestionAdin(object):
    '''章节问题'''
    list_display = ['user', 'lesson', 'questions', 'add_time']
    search_fields = ['user', 'lesson', 'questions']
    list_filter = ['user', 'lesson', 'questions', 'add_time']


class UserFavoriteAdmin(object):
    '''用户收藏后台'''

    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


# 将后台管理器与models进行关联注册。
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(LessonQuestion,LessonQuestionAdin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)