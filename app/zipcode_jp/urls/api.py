# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from zipcode_jp.views import api


# djangorestframework 2.4.4 にバグがあって、キャッシュを使うとエラーになる。修正されるみたい。
# https://github.com/tomchristie/django-rest-framework/issues/1850
if settings.DEBUG:
    CACHE_BASE_SECONDS = 5
else:
    CACHE_BASE_SECONDS = 60

urlpatterns = [
    url(
        r'^$',
        cache_page(CACHE_BASE_SECONDS)(api.ZipCodeList.as_view()),
        name='zipcode_jp-home'
    ),
    url(
        r'^search$',
        cache_page(CACHE_BASE_SECONDS)(api.ZipCodeSearchList.as_view())
    ),
    url(
        r'^(?P<code>[0-9]+)/$',
        cache_page(CACHE_BASE_SECONDS)(api.ZipCodeDetail.as_view()),
        name='zipcode_jp-detail'
    ),
    url(
        r'^(?P<prefecture>\w+)/$',
        cache_page(CACHE_BASE_SECONDS)(api.ZipCodeRegionList.as_view())
    ),
    url(
        r'^(?P<prefecture>\w+)/(?P<city>\w+)/$',
        cache_page(CACHE_BASE_SECONDS)(api.ZipCodeRegionList.as_view())
    ),
    url(
        r'^(?P<prefecture>\w+)/(?P<city>\w+)/(?P<town>\w+)/$',
        cache_page(CACHE_BASE_SECONDS)(api.ZipCodeRegionList.as_view())
    ),
]
