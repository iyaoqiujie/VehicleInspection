# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-25 08:48

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class UserProfile(AbstractUser):
    TYPE_CHOICES = (
        ('SUPERADMIN', '超级管理员'),
        ('STATIONADMIN', '检查点管理员'),
        ('CLIENT', '普通用户')
    )
    mobile = models.CharField(verbose_name='移动电话', blank=True, max_length=16, unique=True, help_text='手机号码')
    # 用户注册时我们要新建user_profile 但是我们只有手机号
    name = models.CharField(verbose_name='姓名', max_length=32, blank=True)
    email = models.EmailField(verbose_name='电子邮箱', max_length=128, blank=True)
    company = models.CharField(verbose_name='所属公司', max_length=128, blank=True)
    usertype = models.CharField(verbose_name='用户类型', max_length=16, choices=TYPE_CHOICES, default='CLIENT')
    #avatar = models.URLField(verbose_name="头像", blank=True)
    avatar = models.ImageField(verbose_name='头像', upload_to='avatar', default='/static/avatar/head.gif')
    is_certificated = models.BooleanField(verbose_name='是否已完成实名认证', default=False)

    credit = models.IntegerField(verbose_name="信用级别", default=100)
    can_order = models.BooleanField(verbose_name="能否预约", default=False)
    ban_start = models.DateTimeField(verbose_name="开始封禁的时间", blank=True, null=True)
    ban_days = models.IntegerField(verbose_name="封禁天数", default=0)

    class Meta:
        db_table = 'UserProfile'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码,回填验证码进行验证。可以保存在redis中
    """
    code = models.CharField(verbose_name="验证码", max_length=10)
    mobile = models.CharField(verbose_name="电话", max_length=16)
    created = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)

    class Meta:
        db_table = 'VerifyCode'
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}:{}'.format(self.mobile, self.code)
