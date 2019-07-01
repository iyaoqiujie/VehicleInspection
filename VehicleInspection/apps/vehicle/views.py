# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-27 23:23

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
from .models import Vehicle
from .serializers import VehicleSerializer

import logging
User = get_user_model()
myLogger = logging.getLogger('insp.vechicle')


class CustomerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class VehicleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [permissions.IsAuthenticated]
    #pagination_class = CustomerPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('vtype', 'character',)
    search_fields = ('vin', 'plate', 'bound_user__name', 'bound_user__mobile')
    ordering_fields = ('created',)

    def get_queryset(self):
        if self.request.user.usertype == 'client':
            return Vehicle.objects.filter(bound_user=self.request.user)
        else:
            return Vehicle.objects.all()
