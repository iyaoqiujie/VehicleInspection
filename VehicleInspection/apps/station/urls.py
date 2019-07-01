# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-26 09:10

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'inspstation', views.InspStationViewSet)
router.register(r'apprule', views.AppointmentRuleViewSet)
router.register(r'appday', views.AppointmentDayViewSet)
#
urlpatterns = [
    path('', include(router.urls)),
]
