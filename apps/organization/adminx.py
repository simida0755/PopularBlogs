# organization/adminx.py

import xadmin

from .models import  BlogOrg, Blogger




class BlogOrgAdmin(object):
    '''平台'''

    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums',  'add_time']


class BloggerAdmin(object):
    '''博主'''

    list_display = ['name', 'org', 'work_years', 'blog_url','work_company', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'blog_url','work_company']
    list_filter = ['org__name', 'name', 'work_years', 'blog_url','work_company', 'click_nums', 'fav_nums', 'add_time']



xadmin.site.register(BlogOrg, BlogOrgAdmin)
xadmin.site.register(Blogger, BloggerAdmin)