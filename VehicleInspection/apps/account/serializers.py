# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-04-16 08:48

import re
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from VehicleInspection.settings import REGEX_MOBILE
from .models import VerifyCode
import logging

User = get_user_model()
myLogger = logging.getLogger('insp.account')


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=16)

    def validate_mobile(self, value):
        """
        验证手机号码(函数名称必须为validate_ + 字段名)
        """
        # 手机是否注册
        if User.objects.filter(mobile=value).count():
            raise serializers.ValidationError('用户已经存在')

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, value):
            raise serializers.ValidationError('手机号码非法')

        # 验证码发送频率
        two_minutes_ago = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)
        # 添加时间大于2分钟以前。也就是距离现在还不足2分钟
        if VerifyCode.objects.filter(created__gt=two_minutes_ago, mobile=value).count():
            raise serializers.ValidationError('距离上一次发送未超过120秒')

        return value


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='用户名', help_text='请输入用户名', required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])
    password = serializers.CharField(label='密码', help_text='密码', write_only=True, style={'input_type': 'password'})
    mobile = serializers.CharField(label='手机号码', help_text='手机号码', required=True, write_only=True,)
    smscode = serializers.CharField(label='验证码', required=True, write_only=True, max_length=4, min_length=4,
                                    error_messages={
                                         'blank': '请输入验证码',
                                         'required': '请输入验证码',
                                         'max_length': '验证码格式错误',
                                         'min_length': '验证码格式错误'
                                    }, help_text='验证码')
    code = serializers.IntegerField(default=20000, read_only=True)

    def validate_smscode(self, code):
        # get与filter的区别: get有两种异常，一个是有多个，一个是一个都没有。
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data['username'], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # 验证码在数据库中是否存在，用户从前端post过来的值都会放入initial_data里面，排序(最新一条)。
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['mobile']).order_by('-created')
        if verify_records:
            # 获取到最新一条
            last_record = verify_records[0]

            # 有效期为五分钟。
            five_minutes_ago = timezone.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.created:
                raise serializers.ValidationError('验证码过期')

            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')

        else:
            raise serializers.ValidationError('验证码错误')

    # 不加字段名的验证器作用于所有字段之上。attrs是字段 validate之后返回的总的dict
    def validate(self, attrs):
        del attrs['smscode']
        return attrs

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    mobile=validated_data['mobile'],)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password', 'smscode')


class UserAddSerializer(serializers.ModelSerializer):
    """
    Admin用户手动添加用户，用户初始密码为123456
    """
    username = serializers.CharField(label="用户名", help_text="请输入用户名", required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    mobile = serializers.CharField(label="手机号码", help_text="手机号码", required=True, write_only=True, )
    code = serializers.IntegerField(default=20000, read_only=True)

    def validate(self, attrs):
        myLogger.debug(attrs)
        return attrs

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    mobile=validated_data['mobile'],
                    name=validated_data['name'],
                    email=validated_data['email'],
                    company=validated_data['company'],
                    role=validated_data['role'],
                    is_certificated=validated_data['is_certificated'])
        user.set_password('123456')
        user.save()
        return user

    class Meta:
        model = User
        fields = ('code', 'username', 'name', 'mobile', 'email', 'company', 'role', 'is_certificated')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """

    username = serializers.ReadOnlyField()
    code = serializers.IntegerField(default=20000, read_only=True)

    class Meta:
        model = User
        fields = ('code', 'id', 'username', 'mobile', 'email', 'company', 'avatar', 'role',
                  'id_card', 'is_certificated', 'can_order', 'date_joined')
