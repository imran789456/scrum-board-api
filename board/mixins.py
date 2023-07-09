from . import models, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, permissions, filters

class DefaultMixin:
    """Default settings for view authentication, permissions,
filtering and pagination."""

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    """
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    """