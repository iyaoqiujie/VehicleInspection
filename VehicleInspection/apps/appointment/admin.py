# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-26 08:59

from django.contrib import admin
from django.contrib.auth import get_user_model
#from guardian.admin import GuardedModelAdmin
from .models import AppointmentOrder, AppmntOrderAgg

import logging

# Register your models here.

User = get_user_model()
myLogger = logging.getLogger('insp.appointment')


@admin.register(AppointmentOrder)
class AppointmentOrderAdmin(admin.ModelAdmin):
    fields = ('order_user', 'plate', 'vin', 'station', 'scheduled_date', 'scheduled_time_period', 'service', 'status')
    raw_id_fields = ('order_user', 'station')
    list_display = ('order_user', 'plate', 'vin', 'station', 'scheduled_date', 'scheduled_time_period', 'service', 'status', 'created')
    list_filter = ('station', 'scheduled_date', 'service', 'status')
    search_fields = ('order_user',)
    ordering = ('-created',)
    list_per_page = 20


@admin.register(AppmntOrderAgg)
class AppmntOrderAggAdmin(admin.ModelAdmin):
    fields = ('station', 'scheduled_date', 'scheduled_time_period', 'order_count')
    raw_id_fields = ('station',)
    list_display = ('station', 'scheduled_date', 'scheduled_time_period', 'order_count')
    list_filter = ('station', 'scheduled_date', 'scheduled_time_period',)
    ordering = ('-scheduled_date',)
    list_per_page = 20
