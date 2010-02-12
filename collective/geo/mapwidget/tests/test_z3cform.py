import unittest
from zope.testing import doctest
from collective.geo.mapwidget.tests import base

import collective.geo.mapwidget.z3cform

def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.mapwidget.z3cform,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ))
