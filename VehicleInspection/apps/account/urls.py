# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-04-16 09:37

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SmsCodeViewSet, UserViewSet, UserAddViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'code', SmsCodeViewSet, base_name='code')
router.register(r'addUser', UserAddViewSet, base_name='add_user')

urlpatterns = [
    path('', include(router.urls)),
]