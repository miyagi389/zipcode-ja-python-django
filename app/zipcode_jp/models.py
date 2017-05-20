# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel


class ZipCodeManager(models.Manager):
    def search(self, search_key):
        q = self.filter(
            Q(jis_code__icontains=search_key) |
            Q(code__icontains=search_key) |
            Q(prefecture_kana__icontains=search_key) |
            Q(city_kana__icontains=search_key) |
            Q(town_kana__icontains=search_key) |
            Q(prefecture__icontains=search_key) |
            Q(city__icontains=search_key) |
            Q(town__icontains=search_key)
        )
        return q


@python_2_unicode_compatible
class ZipCode(TimeStampedModel):
    """
    郵便局が提供している郵便番号データを格納する。
    see: http://www.post.japanpost.jp/zipcode/dl/readme.html
    """

    objects = ZipCodeManager()

    jis_code = models.CharField(
        max_length=10,
        blank=False,
        verbose_name="全国地方公共団体コード(JIS X0401、X0402)",
    )
    old_code = models.CharField(
        max_length=5,
        blank=False,
        verbose_name="郵便番号(旧)",
    )
    code = models.CharField(
        max_length=7,
        blank=False,
        db_index=True,
        verbose_name="郵便番号(新)",
    )
    prefecture_kana = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="都道府県名(カナ)",
    )
    city_kana = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="市区町村名(カナ)",
    )
    town_kana = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="町域名(カナ)",
    )
    prefecture = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="都道府県名",
    )
    city = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="市区町村名",
    )
    town = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="町域名",
    )
    town_divide = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="一町域が二以上の郵便番号で表される場合の表示",
        help_text="1:該当、0:該当せず",
    )
    koaza_banchi = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="小字毎に番地が起番されている町域の表示",
        help_text="1:該当、0:該当せず",
    )
    tyoume = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="丁目を有する町域の場合の表示。",
        help_text="1:該当、0:該当せず",
    )
    has_some_town = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="一つの郵便番号で二以上の町域を表す場合の表示",
        help_text="1:該当、0:該当せず",
    )
    update_state = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="更新の表示",
        help_text="0:変更なし、1:変更あり、2:廃止(廃止データのみ使用)",
    )
    update_reason = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="変更理由",
        help_text="0:変更なし、1:市政・区政・町政・分区・政令指定都市施行、2:住居表示の実施、3:区画整理、4:郵便区調整等、5:訂正、6:廃止(廃止データのみ使用)",
    )

    def __str__(self):
        return "{code} {prefecture} {city} {town}".format(
            code=self.code,
            prefecture=self.prefecture,
            city=self.city,
            town=self.town
        )

