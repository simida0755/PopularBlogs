# organization/urls.py

from organization.views import AddUserAskView,BloggerListView,BloggerHomeView,AddFavView,BloggerDescView,BloggerPostsView,BloggerCourseView

from django.urls import path,re_path

# 要写上app的名字
app_name = "organization"

urlpatterns = [
    path('list/',BloggerListView.as_view(),name='blogger_list'),
    re_path('home/(?P<blogger_id>\d+)/', BloggerHomeView.as_view(), name="blogger_home"),
    re_path('posts/(?P<blogger_id>\d+)/', BloggerPostsView.as_view(), name="blogger_posts"),
    re_path('course/(?P<blogger_id>\d+)/', BloggerCourseView.as_view(), name="blogger_course"),
    re_path('desc/(?P<blogger_id>\d+)/', BloggerDescView.as_view(), name="blogger_desc"),
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
]