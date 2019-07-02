# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-25 16:15

from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
myLogger = logging.getLogger('insp.station')


class InspStation(models.Model):
    id = models.BigAutoField(primary_key=True)
    admin = models.OneToOneField(User, related_name='station', on_delete=models.CASCADE, verbose_name='管理员')
    name = models.CharField(verbose_name='检测站名称', max_length=64,  unique=True)
    contact = models.CharField(verbose_name='联系人', max_length=64,  blank=True)
    phone = models.CharField(verbose_name='电话', max_length=64, blank=True)
    address = models.CharField(verbose_name='地址', max_length=256, blank=True)
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'InspStation'
        verbose_name = '车辆检测站'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '车辆检测站({}), 管理员({})'.format(self.name, self.admin.username)


class AppointmentDay(models.Model):
    id = models.BigAutoField(primary_key=True)
    station = models.ForeignKey(InspStation, related_name='appointmentDays', on_delete=models.CASCADE,
                                db_column='station_id', null=False, blank=False, verbose_name='车辆检测站')
    day = models.DateField(verbose_name='日期', null=False, blank=False, unique=True)
    can_order = models.BooleanField(verbose_name='能否预约', default=True)
    remark = models.CharField(verbose_name='备注', max_length=128, blank=True)



    @classmethod
    def create(cls, station, day):
        isWorkday = True
        if day.weekday() == 5 or day.weekday() == 6:
            isWorkday = False

        return cls(station=station, day=day, can_order=isWorkday)

    class Meta:
        db_table = 'AppointmentDay'
        verbose_name = '预约时间'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '车辆检测站({}), {}'.format(self.station.name, self.day)


def incre_time(start_time, interval):
    start_hour = start_time.hour
    start_minute = start_time.minute
    if interval == 60:
        my_hour = start_hour + 1
        if my_hour >= 24:
            my_hour -= 24

        return start_time.replace(hour=my_hour, minute=start_minute), start_time
    elif interval == 90:
        my_hour = start_hour + 1
        my_minute = start_minute + 30
        if my_minute >= 60:
            my_minute -= 60
            my_hour += 1
        if my_hour >= 24:
            my_hour -= 24

        return start_time.replace(hour=my_hour, minute=my_minute), start_time
    elif interval == 120:
        my_hour = start_hour + 2
        if my_hour >= 24:
            my_hour -= 24

        return start_time.replace(hour=my_hour, minute=start_minute), start_time
    else:
        myLogger.error('Invalid time interval:[{} minutes]. We will use 1 hour instead.'.format(interval))

        my_hour = start_hour + 1
        if my_hour >= 24:
            my_hour -= 24

        return start_time.replace(hour=my_hour, minute=start_minute), start_time


class AppointmentRule(models.Model):
    INTERVAL_CHOICES = (
        (60, '1小时'),
        (90, '1个半小时'),
        (120, '2小时')
    )
    id = models.BigAutoField(primary_key=True)
    station = models.OneToOneField(InspStation, related_name='appointmentRule', on_delete=models.CASCADE,
                                   db_column='station_id', null=False, blank=False, verbose_name='车辆检测站')
    am_start_time = models.TimeField(verbose_name='上午检测开始时间', default='08:00')

    am_end_time = models.TimeField(verbose_name='上午检测结束时间', default='11:00')
    pm_start_time = models.TimeField(verbose_name='下午检测开始时间', default='13:00')
    pm_end_time = models.TimeField(verbose_name='下午检测结束时间', default='17:00')
    cutoff_time = models.TimeField(verbose_name='当天截止预约时间', default='16:00')
    interval = models.IntegerField(verbose_name='时间间隔', choices=INTERVAL_CHOICES, default=60)
    threshold = models.IntegerField(verbose_name='单个时间段最大预约数', default=20)

    class Meta:
        db_table = 'AppointmentRule'
        verbose_name = '预约规则'
        verbose_name_plural = verbose_name

    def time_periods(self):
        periods = []

        # AM
        end_time = self.am_start_time
        while end_time < self.am_end_time:
            end_time, start_time = incre_time(end_time, self.interval)
            if end_time <= self.am_end_time:
                periods.append('{} - {}'.format(start_time.strftime('%H:%M'), end_time.strftime('%H:%M')))

        # PM
        end_time = self.pm_start_time
        while end_time < self.pm_end_time:
            end_time, start_time = incre_time(end_time, self.interval)
            if end_time <= self.pm_end_time:
                periods.append('{} - {}'.format(start_time.strftime('%H:%M'), end_time.strftime('%H:%M')))

        return periods

    def __str__(self):
        return '车辆检测站({})预约规则'.format(self.station.name)
