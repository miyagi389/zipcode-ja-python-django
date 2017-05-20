# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import serializers

from zipcode_jp.models import ZipCode


class ZipCodeSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedIdentityField(
        view_name='zipcode_jp-detail',
        lookup_field='code',
        help_text='郵便番号リソースへのリンク',
    )

    class Meta:
        model = ZipCode
        fields = (
            'link',
            'jis_code',
            'code',
            'prefecture_kana',
            'city_kana',
            'town_kana',
            'prefecture',
            'city',
            'town',
        )
