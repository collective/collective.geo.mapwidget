import unittest
from zope.testing import doctest

import collective.geo.mapwidget.geoconfig

from zope.component import provideUtility
from collective.geo.mapwidget import geoconfig
from collective.geo.mapwidget import interfaces


def setUp(test):
    provideUtility(
              geoconfig.GeoSettings,
              provides = interfaces.IGeoSettings)


def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.mapwidget.geoconfig,
                     setUp=setUp,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)))
