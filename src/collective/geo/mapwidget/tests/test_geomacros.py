import urllib
import unittest2 as unittest
from decimal import Decimal

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.geo.settings.interfaces import IGeoSettings

from ..testing import CGEO_MAPWIDGET_INTEGRATION


class TestSetupHTTP(unittest.TestCase):
    layer = CGEO_MAPWIDGET_INTEGRATION

    _protocol = 'http'

    def setUp(self):
        self.portal = self.layer['portal']
        self._old_request_url = self.portal.REQUEST.getURL()
        self.portal.REQUEST.setServerURL(self._protocol, 'nohost')
        self.settings = self.portal.restrictedTraverse('@@geosettings-view')
        self.geosettings = getUtility(IRegistry).forInterface(IGeoSettings)

    def beforeTearDown(self):
        url_parts = urllib.splittype(self._old_request_url)
        self.portal.REQUEST.setServerURL(*url_parts)

    def test_property_zoom(self):
        self.assertEquals(self.settings.zoom, Decimal("10.0"))

    def test_property_map_center(self):
        self.assertEquals(
            self.settings.map_center,
            (Decimal("0.00"), Decimal("0.0"))
        )

    def test_property_googleapi(self):
        key = u'ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-'\
              'All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw'
        self.assertEquals(self.settings.googleapi, key)

    def test_property_jsgooglemaps(self):
        # when a layer is google_map we should include external javascript
        self.geosettings.default_layers = [u'google_map']
        self.assertEquals(
            self.settings.google_maps_js,
            '%s://maps.google.com/maps/api/js?v=3.2&sensor=false' %
            self._protocol
        )

        self.geosettings.default_layers = [u'osm']
        self.assertFalse(self.settings.googlemaps)

    def test_property_jsbingmaps(self):
        # when a layer is bing_map we should include external javascript
        self.geosettings.default_layers = [u'bing_map']
        self.assertEquals(
            self.settings.bing_maps_js,
            '%s://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6' %
            self._protocol
        )

        self.geosettings.default_layers = [u'osm']
        self.assertFalse(self.settings.bingmaps)

    def test_geosettings_properties(self):
        self.assertEqual(
            self.settings.zoom,
            10
        )

        self.assertEqual(
            self.settings.map_center,
            (Decimal('0.0'), Decimal('0.0'))
        )

        self.assertEqual(
            self.settings.imgpath,
            "string:${portal_url}/img/"
        )


class TestSetupHTTPS(TestSetupHTTP):
    _protocol = 'https'


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetupHTTP))
    suite.addTest(unittest.makeSuite(TestSetupHTTPS))
    return suite
