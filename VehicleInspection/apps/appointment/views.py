# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-26 14:15

from django.contrib.auth import get_user_model
from rest_framework import generics, renderers, permissions, viewsets, mixins, status
from rest_framework.pagination import PageNumberPagination, PageLink
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
# Search, Ordering, Filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import datetime, xlrd, re
# Auth
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django_redis import get_redis_connection, cache
from .models import AppointmentOrder, AppmntOrderAgg
from station.permissions import IsStationAdmin
from .serializers import AppointmentOrderSerializer, AppmntOrderAggSerializer

import logging
User = get_user_model()
myLogger = logging.getLogger('insp.appointment')


class CustomerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class AppointmentOrderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = AppointmentOrder.objects.all()
    serializer_class = AppointmentOrderSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [permissions.IsAuthenticated]
    #pagination_class = CustomerPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('station__admin', 'station__id', 'station__name', 'scheduled_date', 'service', 'status')
    search_fields = ('order_user__name', 'order_user__mobile')
    ordering_fields = ('scheduled_date',)

    def get_queryset(self):
        if self.request.user.role == 'CLIENT':
            return AppointmentOrder.objects.filter(order_user=self.request.user)
        elif self.request.user.role == 'STATIONADMIN':
            return AppointmentOrder.objects.filter(station=self.request.user.station)
        else:
            return AppointmentOrder.objects.all()


class AppmntOrderAggViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset for read only
    """
    queryset = AppmntOrderAgg.objects.all()
    serializer_class = AppmntOrderAggSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAdminUser | IsStationAdmin, ]
    #pagination_class = CustomerPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('station__name', 'scheduled_date',)
    ordering_fields = ('-scheduled_date',)

    def get_queryset(self):
        if self.request.user.role == 'STATIONADMIN':
            return AppmntOrderAgg.objects.filter(station=self.request.user.station)
        else:
            return AppmntOrderAgg.objects.all()

