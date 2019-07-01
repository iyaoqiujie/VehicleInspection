# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-04-16 08:48

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, VerifyCode
import logging

myLogger = logging.getLogger('insp.account')
# Register your models here.


class UserProfileAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('personal info', {'fields': ('first_name', 'last_name', 'name', 'mobile',
                                      'email', 'company', 'avatar', 'usertype', 'is_certificated')}),
        ('permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('credit', {'fields': ('credit', 'can_order', 'ban_start', 'ban_days')}),
        (None, {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'name', 'mobile', 'usertype', 'is_certificated', 'credit', 'can_order',
                    'last_login', 'date_joined')
    list_filter = ('is_certificated', 'usertype', 'can_order')
    search_fields = ('username', 'name', 'mobile', 'company')
    ordering = ('-last_login', '-date_joined', )


@admin.register(VerifyCode)
class VerifyCodeAdmin(admin.ModelAdmin):
    fields = ('code', 'mobile')
    list_display = ('code', 'mobile', 'created')
    search_fields = ('mobile',)
    ordering = ('-created',)


admin.site.site_header = '车辆检测预约管理系统'
admin.site.site_title = '车辆检测预约管理系统'
admin.site.register(UserProfile, UserProfileAdmin)
