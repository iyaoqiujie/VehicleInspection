# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-25 16:15

from django.contrib import admin
from django.contrib.auth import get_user_model
#from guardian.admin import GuardedModelAdmin
from .models import InspStation, AppointmentDay, AppointmentRule

import logging

# Register your models here.

User = get_user_model()
myLogger = logging.getLogger('insp.station')


@admin.register(InspStation)
class InspStationAdmin(admin.ModelAdmin):
    fields = ('admin', 'name', 'contact', 'phone', 'address')
    raw_id_fields = ('admin',)
    list_display = ('name', 'contact', 'phone', 'address', 'created')
    search_fields = ('name', 'contact', 'phone', 'address')
    ordering = ('-created',)
    list_per_page = 20


@admin.register(AppointmentDay)
class AppointmentDayAdmin(admin.ModelAdmin):
    fields = ('day', 'can_order', 'remark', 'station')
    raw_id_fields = ('station',)
    list_display = ('day', 'can_order', 'remark', 'station')
    ordering = ('day',)
    list_per_page = 20


@admin.register(AppointmentRule)
class AppointmentRuleAdmin(admin.ModelAdmin):
    fields = ('am_start_time', 'am_end_time', 'pm_start_time', 'pm_end_time', 'cutoff_time',
              'interval', 'threshold', 'station')
    raw_id_fields = ('station',)
    list_display = ('am_start_time', 'am_end_time', 'pm_start_time', 'pm_end_time', 'cutoff_time',
                    'interval', 'threshold', 'station')
    list_per_page = 20
