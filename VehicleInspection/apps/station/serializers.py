# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-25 16:15

import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_redis import cache, get_redis_connection
from django.db.models import Q
from VehicleInspection.settings import REGEX_MOBILE
from .models import InspStation, AppointmentRule, AppointmentDay
import logging

User = get_user_model()
myLogger = logging.getLogger('insp.station')


class InspStationSerializer(serializers.ModelSerializer):
    #appointmentDays = serializers.HyperlinkedRelatedField(many=True, view_name='appointmentday-detail',
    #                                                      read_only=True)
    appointmentRule = serializers.HyperlinkedRelatedField(many=False, view_name='appointmentrule-detail',
                                                          read_only=True)
    #appointmentOrders = serializers.HyperlinkedRelatedField(many=True, view_name='appointmentorder-detail',
    #                                                        read_only=True)
    appmntOrderAgg = serializers.HyperlinkedRelatedField(many=True, view_name='appmntorderagg-detail',
                                                         read_only=True)
    admin_username = serializers.ReadOnlyField(source='admin.username')
    stationadmin = serializers.CharField(label='检测点管理员', write_only=True, required=True,
                                         error_messages={
                                             'blank': '请输入检测点管理员用户名或手机号',
                                             'required': '请输入检测点管理员用户名或手机号'
                                         }, help_text='检测点管理员用户名或手机号')
    code = serializers.IntegerField(default=20000, read_only=True)

    def validate_stationadmin(self, value):
        try:
            user = User.objects.get(Q(username=value) | Q(mobile=value))
            if user.usertype != 'STATIONADMIN':
                raise serializers.ValidationError('用户[{}]不是检测点管理员'.format(value))
        except User.MultipleObjectsReturned as me:
            myLogger.warning('Multi users retrieved for username [{}]'.format(value))
            raise serializers.ValidationError('用户名[{}]非法'.format(value))
        except User.DoesNotExist as ne:
            myLogger.warning('No user found  for username [{}]'.format(value))
            raise serializers.ValidationError('用户[{}]不存在'.format(value))

        return value

    def create(self, validated_data):
        sAdmin = User.objects.get(Q(username=validated_data['stationadmin']) | Q(mobile=validated_data['stationadmin']))
        # Create Station
        station = InspStation(admin=sAdmin,
                              name=validated_data['name'],
                              address=validated_data['address'],
                              contact=validated_data['contact'],
                              phone=validated_data['phone'],)
        station.save()

        # Once station was created, create its appointment rule
        rule = AppointmentRule(station=station)
        rule.save()

        return station

    class Meta:
        model = InspStation
        fields = ('code', 'admin_username', 'id', 'stationadmin', 'name', 'contact', 'phone', 'address', 'created',
                  'appointmentRule', 'appmntOrderAgg')


class AppointmentRuleSerializer(serializers.ModelSerializer):
    station_name = serializers.ReadOnlyField(source='station.name')
    station_id = serializers.ReadOnlyField(source='station.id')
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
