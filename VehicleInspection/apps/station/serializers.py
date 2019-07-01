# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-25 16:15

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_redis import cache, get_redis_connection
from .models import InspStation, AppointmentRule, AppointmentDay
import logging

User = get_user_model()
myLogger = logging.getLogger('insp.station')


class InspStationSerializer(serializers.ModelSerializer):
    appointmentDays = serializers.HyperlinkedRelatedField(many=True, view_name='appointmentday-detail',
                                                          read_only=True)
    appointmentRule = serializers.HyperlinkedRelatedField(many=False, view_name='appointmentrule-detail',
                                                          read_only=True)
    appointmentOrders = serializers.HyperlinkedRelatedField(many=True, view_name='appointmentorder-detail',
                                                            read_only=True)
    appmntOrderAgg = serializers.HyperlinkedRelatedField(many=True, view_name='appmntorderagg-detail',
                                                         read_only=True)
    admin_username = serializers.ReadOnlyField(source='admin.username')
    code = serializers.IntegerField(default=20000, read_only=True)

    class Meta:
        model = InspStation
        fields = ('code', 'admin_username', 'id', 'name', 'contact', 'phone', 'address', 'created',
                  'appointmentDays', 'appointmentRule', 'appointmentOrders', 'appmntOrderAgg')


class AppointmentRuleSerializer(serializers.ModelSerializer):
    station_name = serializers.ReadOnlyField(source='station.name')
    code = serializers.IntegerField(default=20000, read_only=True)

    class Meta:
        model = AppointmentRule
        fields = '__all__'


class AppointmentDaySerializer(serializers.ModelSerializer):
    station_name = serializers.ReadOnlyField(source='station.name')
    code = serializers.IntegerField(default=20000, read_only=True)

    class Meta:
        model = AppointmentDay
        fields = '__all__'
