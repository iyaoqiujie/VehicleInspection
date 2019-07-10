# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-25 16:15

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
from .permissions import ReadOnly, IsOwnerOrReadOnly
from .models import InspStation, AppointmentDay, AppointmentRule
from .serializers import InspStationSerializer, AppointmentRuleSerializer, AppointmentDaySerializer

import logging
User = get_user_model()
myLogger = logging.getLogger('insp.station')


class CustomerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class InspStationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = InspStation.objects.all()
    serializer_class = InspStationSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAdminUser | ReadOnly]
    #pagination_class = CustomerPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name', 'contact', 'phone', 'address')
    ordering_fields = ('created',)

    @action(detail=False, methods=['get'])
    def fetch_station(self, request):
        try:
            my_station = self.request.user.station
            serializer = self.get_serializer(my_station)
            return Response(serializer.data)
        except User.station.RelatedObjectDoesNotExist:
            return Response({'code': 20000, 'message': 'You have no vehicle station in charge'})

    @action(detail=True, methods=['get'])
    def time_periods(self, request, pk=None):
        station = self.get_object()
        periods = station.appointmentRule.time_periods()
        return Response({'code': 20000, 'periods': periods})


class DateRangeFilter(filters.BaseFilterBackend):
    """
    根据输入的时间范围来过滤
    字段: [start_day, end_day]
    """
    def filter_queryset(self, request, queryset, view):
        start = request.query_params.get('start') or ''
        end = request.query_params.get('end') or ''

        try:
            start_day = datetime.datetime.strptime(start, '%Y-%m-%d')
        except ValueError as ve:
            start_day = datetime.date.today()

        try:
            end_day = datetime.datetime.strptime(end, '%Y-%m-%d')
        except ValueError as ve:
            end_day = start_day + datetime.timedelta(days=6)

        myLogger.debug("start_day: {}, end_day: {}".format(start_day, end_day))
        return queryset.filter(day__gte=start_day).filter(day__lte=end_day)


class AppointmentDayViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = AppointmentDay.objects.all()
    serializer_class = AppointmentDaySerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsOwnerOrReadOnly]
    #pagination_class = CustomerPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, DateRangeFilter)
    filter_fields = ('day', 'weekday', 'can_order', 'station')
    search_fields = ('station__name', )
    ordering_fields = ('day',)

    def get_queryset(self):
        if self.request.user.role == 'STATIONADMIN':
            return AppointmentDay.objects.filter(station=self.request.user.station)
        else:
            return AppointmentDay.objects.all()


class AppointmentRuleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = AppointmentRule.objects.all()
    serializer_class = AppointmentRuleSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsOwnerOrReadOnly]
    #pagination_class = CustomerPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('station__name', )
    ordering_fields = ('station__created',)

    @action(detail=False, methods=['get'])
    def fetch_rule(self, request):
        try:
            my_station = self.request.user.station
            serializer = self.get_serializer(my_station.appointmentRule)
            return Response(serializer.data)
        except User.station.RelatedObjectDoesNotExist:
            return Response({'code': 20000, 'message': 'You have no vehicle station in charge'})

    def get_queryset(self):
        if self.request.user.role == 'STATIONADMIN':
            return AppointmentRule.objects.filter(station=self.request.user.station)
        elif self.request.user.role == 'SUPERADMIN':
            return AppointmentRule.objects.all()
        else:
            return AppointmentRule.objects.none()
