# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import locale
import logging
import os
import re
import tempfile
import zipfile

from django.db import transaction
import requests
import zenhan
from django.core.management.base import BaseCommand
from six import StringIO

from zipcode_jp.models import ZipCode


class Command(BaseCommand):
    """
    Import an japanease zip code into the app.
    """

    ZIP_FILE_URL = "http://www.post.japanpost.jp/zipcode/dl/oogaki/zip/ken_all.zip"
    ZIP_FILE_NAME = "KEN_ALL.CSV"

    logger = logging.getLogger('app')

    help = ("郵便局Webサイト(http://www.post.japanpost.jp/zipcode/download.html) から "
            "郵便番号データをダウンロードしてデータベースにインポートします。")

    def add_arguments(self, parser):
        parser.add_argument('--include_zipcode_regex', nargs='?', default=None, help='include zipcode regex pattern')

    def handle(self, *app_labels, **options):
        self.logger.info("start.")
        zip_temp_file = None
        try:
            self.logger.info("downloading: %s", self.ZIP_FILE_URL)
            response = requests.get(self.ZIP_FILE_URL)
            self.logger.info("downloaded: %s", self.ZIP_FILE_URL)

            zip_temp_file = tempfile.NamedTemporaryFile(delete=False)
            self.logger.info("writing: %s", zip_temp_file.name)
            zip_temp_file.write(response.content)
            zip_temp_file.close()
            self.logger.info("written: %s, size: %d", zip_temp_file.name, os.path.getsize(zip_temp_file.name))

            with zipfile.ZipFile(zip_temp_file.name, 'r') as zip_file:
                include_zipcode_regex = options['include_zipcode_regex']
                f = StringIO(zip_file.read(self.ZIP_FILE_NAME).decode("ms932"))
                self.read_csv_and_write_database(include_zipcode_regex, f)
        except requests.exceptions.RequestException:
            self.logger.exception("download error")
        finally:
            if zip_temp_file is not None and os.path.isfile(zip_temp_file.name):
                os.remove(zip_temp_file.name)

        self.logger.info("end.")

    @transaction.atomic()
    def read_csv_and_write_database(self, include_zipcode_regex, stream):
        include_zipcode_regex_pattern = re.compile(include_zipcode_regex) if include_zipcode_regex is not None else None
        transaction_save_point = transaction.savepoint()
        try:
            ZipCode.objects.all().delete()

            total = 0

            for line in stream:
                data = line.split(',')

                for idx in range(len(data)):
                    data[idx] = data[idx].strip('" ')

                code = data[2]

                if include_zipcode_regex_pattern is not None:
                    if include_zipcode_regex_pattern.match(code) is None:
                        continue

                o = ZipCode()
                o.jis_code = data[0]
                o.old_code = data[1]
                o.code = code
                o.prefecture_kana = zenhan.h2z(data[3])
                o.city_kana = zenhan.h2z(data[4])
                o.town_kana = zenhan.h2z(data[5])
                o.prefecture = data[6]
                o.city = data[7]
                o.town = data[8]
                o.town_divide = data[9]
                o.koaza_banchi = data[10]
                o.tyoume = data[11]
                o.has_some_town = data[12]
                o.update_state = data[13]
                o.update_reason = data[14]

                o.save()

                total += 1
        except:
            transaction.savepoint_rollback(transaction_save_point)
            raise
        else:
            transaction.savepoint_commit(transaction_save_point)

        locale.setlocale(locale.LC_ALL, "")
        self.logger.info("Total Import: %s", locale.format('%d', total, grouping=True))
