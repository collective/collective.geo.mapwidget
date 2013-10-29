import unittest2 as unittest
import doctest

from zope.component import getGlobalSiteManager
from zope.interface import Interface

from plone.testing import layered

from ..interfaces import IMapLayer
from ..testing import CGEO_MAPWIDGET_FUNCTIONAL


def tearDown(test):  # pylint: disable=W0613
    # unregister image Maplayer
    gsm = getGlobalSiteManager()
    adpt = gsm.queryMultiAdapter(
        (Interface, Interface, Interface, Interface),
        IMapLayer,
        name='image')
    if adpt:
        gsm.unregisterAdapter(
            adpt.__class__,
            (Interface, Interface, Interface, Interface),
            IMapLayer,
            name='image'
        )


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([

        layered(doctest.DocFileSuite(
            'README.txt',
            package='collective.geo.mapwidget',
            tearDown=tearDown,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_MAPWIDGET_FUNCTIONAL
        ),

        layered(doctest.DocFileSuite(
            'controlpanel.txt',
            package='collective.geo.mapwidget.browser',
            tearDown=tearDown,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_MAPWIDGET_FUNCTIONAL
        ),
    ])
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
