# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import doctest

from zipcode_jp import models


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(models))
    return tests
