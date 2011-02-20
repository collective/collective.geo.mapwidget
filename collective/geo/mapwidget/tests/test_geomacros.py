import unittest
from decimal import Decimal
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.geo.mapwidget.tests import base
from collective.geo.settings.interfaces import IGeoSettings


class TestSetup(base.TestCase):

    def afterSetUp(self):
        self.settings = self.portal.restrictedTraverse('@@geosettings-view')
        self.geosettings = getUtility(IRegistry).forInterface(IGeoSettings)

    def test_property_zoom(self):
        self.assertEquals(self.settings.zoom, Decimal("10.0"))

    def test_property_map_center(self):
        self.assertEquals(self.settings.map_center,
                            (Decimal("0.00"), Decimal("0.0")))

    def test_property_googleapi(self):
        self.assertEquals(self.settings.googleapi,
              u'ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw')

    def test_property_jsgooglemaps(self):
        # when a layer is google_map we should include external javascript
        self.geosettings.default_layers = [u'google_map']
        self.assertEquals(self.settings.google_maps_js,
            'http://maps.google.com/maps/api/js?v=3.2&sensor=false')

        self.geosettings.default_layers = [u'osm']
        self.assertEquals(self.settings.google_maps_js, None)

    def test_property_yahooapi(self):
        self.assertEquals(self.settings.yahooapi,
                          u'YOUR_API_KEY')

    def test_property_jsyahoomaps(self):
        # when a layer is yahoo_map we should include external javascript
        self.geosettings.default_layers = [u'yahoo_map']
        self.assertEquals(self.settings.yahoo_maps_js,
              'http://api.maps.yahoo.com/ajaxymap?v=3.8&appid=YOUR_API_KEY')

        self.geosettings.default_layers = [u'osm']
        self.assertEquals(self.settings.yahoo_maps_js, None)

    def test_property_jsbingmaps(self):
        # when a layer is bing_map we should include external javascript
        self.geosettings.default_layers = [u'bing_map']
        self.assertEquals(self.settings.bing_maps_js,
              'http://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6')

        self.geosettings.default_layers = [u'osm']
        self.assertEquals(self.settings.bing_maps_js, None)

    def test_property_geosettingjs(self):
        self.assertEquals(self.settings.geo_setting_js,
            "cgmap.state = {'default': {lon: 0.000000, lat: 0.000000, zoom: 10 }};\n"
            "cgmap.portal_url = 'http://nohost/plone';\n"
            "cgmap.imgpath = '%s/img/';" % self.portal.absolute_url())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
