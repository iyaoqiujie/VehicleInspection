# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-26 09:11

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'order', views.AppointmentOrderViewSet)
router.register(r'orderAgg', views.AppmntOrderAggViewSet)
#
urlpatterns = [
    path('', include(router.urls)),
]
