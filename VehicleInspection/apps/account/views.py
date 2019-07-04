# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-04-16 13:48


from random import choice
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework import viewsets, status
from rest_framework.decorators import action
# Search, Ordering, Filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# 发送验证码是创建model中一条记录的操作
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination, PageLink
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from .models import VerifyCode
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer, UserAddSerializer
from .permissions import IsOwnerOrReadOnly
import logging

User = get_user_model()
myLogger = logging.getLogger('insp.account')

# Create your views here.


class CustomerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except User.MultipleObjectsReturned as me:
            myLogger.warning('Multiple users retrieved!')
        except User.DoesNotExist as ne:
            myLogger.warning('The specified user does NOT exist')

        return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer
    queryset = VerifyCode.objects.all()

    def generate_code(self):
        """
        生成四位数字的验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        code = self.generate_code()
        code_record = VerifyCode(code=code, mobile=mobile)
        code_record.save()
        return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)

# No SMS API yet
#        yun_pian = YunPian(APIKEY)
#        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
#        if sms_status["code"] != 0:
#            return Response({
#                "mobile": sms_status["msg"]
#            }, status=status.HTTP_400_BAD_REQUEST)
#        else:
#            code_record = VerifyCode(code=code, mobile=mobile)
#            code_record.save()
#            return Response({
#                "mobile": mobile
#            }, status=status.HTTP_201_CREATED)


class UserAddViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    手动创建用户
    """
    serializer_class = UserAddSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    #pagination_class = CustomerPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('role', 'can_order', 'is_certificated', 'is_active')
    search_fields = ('name', 'username', 'mobile',)
    ordering_fields = ('last_login', 'date_joined')

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegSerializer
        else:
            return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwnerOrReadOnly | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)



    # TODO
    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAdminUser, IsOwnerOrReadOnly],
            url_path='change-password', url_name='change_password')
    def set_password(self, request, pk=None):
        pass

#    def perform_create(self, serializer):
#        return serializer.save()

