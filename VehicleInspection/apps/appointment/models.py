# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-25 16:16

from django.db import models
from django.contrib.auth import get_user_model

from station.models import InspStation

User = get_user_model()


class AppointmentOrder(models.Model):
    ORDER_STATUS_CHOICES = (
        ('PENDING', '待审核'),
        ('REJECTED', '已拒绝'),
        ('ACTIVE', '进行中'),
        ('CANCELED', '已取消'),
        ('COMPLETED', '已完成'),
    )

    SERVICE_CHOICES = (
        ('INSPECTION', '检测'),
        ('REPAIR', '维修'),
    )

    id = models.BigAutoField(primary_key=True)
    order_user = models.ForeignKey(User, related_name='appointmentOrders', on_delete=models.CASCADE,
                                   db_column='user_id', null=False, blank=False, verbose_name='预约客户')
    station = models.ForeignKey(InspStation, related_name='appointmentOrders', on_delete=models.CASCADE,
                                db_column='station_id', null=False, blank=False, verbose_name='车辆检测站')
    plate = models.CharField(verbose_name='待检机动车车牌号', max_length=16)
    vin = models.CharField(verbose_name='待检机动车识别代码', max_length=32)
    scheduled_date = models.DateField(verbose_name='预约日期', null=False, blank=False, db_index=True)
    scheduled_time_period = models.CharField(verbose_name='预约时间区间', max_length=32, null=False, blank=False)
    service = models.CharField(verbose_name='预约服务', max_length=16, choices=SERVICE_CHOICES, default='INSPECTION')
    status = models.CharField(verbose_name='预约订单状态', max_length=16, choices=ORDER_STATUS_CHOICES, default='PENDING')
    created = models.DateTimeField(verbose_name='预约订单创建时间', auto_now_add=True)

    class Meta:
        db_table = 'AppointmentOrder'
        verbose_name = '预约订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '预约客户[{}, {}], 预约检测点[{}], 预约时间[{}, {}]'.format(
            self.order_user.name,
            self.plate,
            self.station.name,
            self.scheduled_date,
            self.scheduled_time_period,
        )


class AppmntOrderAgg(models.Model):
    id = models.BigAutoField(primary_key=True)
    station = models.ForeignKey(InspStation, related_name='appmntOrderAgg', on_delete=models.CASCADE,
                                db_column='station_id', null=False, blank=False, verbose_name='车辆检测站')
    scheduled_date = models.DateField(verbose_name='预约日期', null=False, blank=False, db_index=True)
    scheduled_time_period = models.CharField(verbose_name='预约时间区间', max_length=32, null=False, blank=False)
    order_count = models.SmallIntegerField(verbose_name='预约数', default=0)

    class Meta:
        db_table = 'AppmntOrderAgg'
        verbose_name = '预约订单汇总'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '预约检测点[{}], 预约时间[{}, {}], 预约数[{}]'.format(
            self.station.name,
            self.scheduled_date,
            self.scheduled_time_period,
            self.order_count
        )
