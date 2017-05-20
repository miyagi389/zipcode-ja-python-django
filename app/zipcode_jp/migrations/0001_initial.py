# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ZipCode',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('jis_code', models.CharField(verbose_name='全国地方公共団体コード(JIS X0401、X0402)', max_length=10)),
                ('old_code', models.CharField(verbose_name='郵便番号(旧)', max_length=5)),
                ('code', models.CharField(db_index=True, verbose_name='郵便番号(新)', max_length=7)),
                ('prefecture_kana', models.CharField(verbose_name='都道府県名(カナ)', max_length=255)),
                ('city_kana', models.CharField(verbose_name='市区町村名(カナ)', max_length=255)),
                ('town_kana', models.CharField(verbose_name='町域名(カナ)', max_length=255)),
                ('prefecture', models.CharField(verbose_name='都道府県名', max_length=255)),
                ('city', models.CharField(verbose_name='市区町村名', max_length=255)),
                ('town', models.CharField(verbose_name='町域名', max_length=255)),
                ('town_divide', models.PositiveSmallIntegerField(help_text='1:該当、0:該当せず', verbose_name='一町域が二以上の郵便番号で表される場合の表示')),
                ('koaza_banchi', models.PositiveSmallIntegerField(help_text='1:該当、0:該当せず', verbose_name='小字毎に番地が起番されている町域の表示')),
                ('tyoume', models.PositiveSmallIntegerField(help_text='1:該当、0:該当せず', verbose_name='丁目を有する町域の場合の表示。')),
                ('has_some_town', models.PositiveSmallIntegerField(help_text='1:該当、0:該当せず', verbose_name='一つの郵便番号で二以上の町域を表す場合の表示')),
                ('update_state', models.PositiveSmallIntegerField(help_text='0:変更なし、1:変更あり、2:廃止(廃止データのみ使用)', verbose_name='更新の表示')),
                ('update_reason', models.PositiveSmallIntegerField(help_text='0:変更なし、1:市政・区政・町政・分区・政令指定都市施行、2:住居表示の実施、3:区画整理、4:郵便区調整等、5:訂正、6:廃止(廃止データのみ使用)', verbose_name='変更理由')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
