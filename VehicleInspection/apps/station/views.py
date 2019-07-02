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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('day', 'can_order', )
    search_fields = ('station__name', )
    ordering_fields = ('day',)


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
        if self.request.user.usertype == 'STATIONADMIN':
            return AppointmentRule.objects.filter(station=self.request.user.station)
        elif self.request.user.usertype == 'SUPERADMIN':
            return AppointmentRule.objects.all()
        else:
            return ''
