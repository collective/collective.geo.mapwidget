import unittest
import doctest

from Testing import ZopeTestCase as ztc

from collective.geo.mapwidget.tests import base


def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'README.txt', package='collective.geo.mapwidget',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ztc.ZopeDocFileSuite(
            'controlpanel.txt', package='collective.geo.mapwidget.browser',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ])
