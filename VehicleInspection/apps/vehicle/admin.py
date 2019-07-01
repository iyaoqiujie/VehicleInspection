# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-27 23:15

from django.contrib import admin
from django.contrib.auth import get_user_model
#from guardian.admin import GuardedModelAdmin
from .models import Vehicle

import logging

# Register your models here.

User = get_user_model()
myLogger = logging.getLogger('insp.vehicle')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    fields = ('plate', 'vin', 'vtype', 'owner', 'character', 'bound_user')
    raw_id_fields = ('bound_user',)
    list_display = ('vin', 'plate', 'vtype', 'owner', 'character', 'bound_user', 'created')
    list_filter = ('vtype', 'character',)
    search_fields = ('vin', 'plate')
    ordering = ('-created',)
