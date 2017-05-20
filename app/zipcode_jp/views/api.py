# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import logging

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.throttling import AnonRateThrottle
from core.mixins import MultipleFieldLookupMixin

from zipcode_jp.models import ZipCode
from zipcode_jp.serializers import ZipCodeSerializer


logger = logging.getLogger(__name__)


class ZipCodeList(ListAPIView):
    """
    郵便番号リソース
    """

    throttle_classes = (AnonRateThrottle,)
    model = ZipCode
    queryset = ZipCode.objects.all().order_by('code')
    serializer_class = ZipCodeSerializer


class ZipCodeDetail(RetrieveAPIView):
    """
    郵便番号リソース
    {code}: 郵便場号(7桁) 例: 1510066
    """

    throttle_classes = (AnonRateThrottle,)
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer
    lookup_field = 'code'


class ZipCodeSearchList(ListAPIView):
    """
    検索結果リソース
    q -- 検索条件
    """

    throttle_classes = (AnonRateThrottle,)
    serializer_class = ZipCodeSerializer

    def list(self, request, *args, **kwargs):
        try:
            search_key = request.QUERY_PARAMS['q']
            self.queryset = ZipCode.objects.search(search_key).order_by('code')
        except KeyError:
            pass
        return super(ZipCodeSearchList, self).list(request, *args, **kwargs)


class ZipCodeRegionList(MultipleFieldLookupMixin, ListAPIView):
    """
    地域リソース
    """

    throttle_classes = (AnonRateThrottle,)
    serializer_class = ZipCodeSerializer
    lookup_fields = ('prefecture', 'city', 'town')

    def list(self, request, *args, **kwargs):
        add_filter = {}
        for field in self.lookup_fields:
            if field in self.kwargs:
                add_filter[field] = self.kwargs[field]

        self.queryset = ZipCode.objects.filter(**add_filter).order_by('code')

        return super(ZipCodeRegionList, self).list(request, *args, **kwargs)
