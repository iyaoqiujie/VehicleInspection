# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-04-16 14:22

from rest_framework import permissions


class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only the company admin to edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        curr_user = request.user

        # Superuser can do everything.
        if curr_user.is_superuser:
            return True

        # Write permissions are allowed to the owner.
        if obj.username == curr_user.username:
            return True

        return curr_user.post == 'admin' and curr_user.company == obj.company


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner.
        return obj.username == request.user.username
