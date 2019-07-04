# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-25 10:57


def jwt_response_payload_handler(token, user=None, request=None):
    """为返回的结果添加用户相关信息"""

    return {
        'code': 20000,
        'token': token,
        'id': user.id,
        'username': user.username,
        'mobile': user.mobile,
        'email': user.email,
        'avatar': user.avatar.url,
        'role': user.role,
        'id_card': user.id_card,
        'is_certificated': user.is_certificated,
        'can_order': user.can_order,
    }
