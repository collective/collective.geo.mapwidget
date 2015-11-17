import unittest
try:
    import json
except ImportError:
    import simplejson as json

from zope.component import getUtility

from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles

from geopy.exc import GeocoderQueryError

from ..utils import GeoCoderUtility
from ..interfaces import IGeoCoder
from ..testing import CGEO_MAPWIDGET_INTEGRATION


test_params = [
    {
        'address': "Torino Italy",
        'output': [
            (u'Metropolitan City of Turin, Italy', (45.070312, 7.686856499999999)),  # noqa
            (u'10040 Torino, Italy', (45.21208780000001, 7.7309388)),
            (u'66020 Torino, Italy', (42.1852556, 14.53967)),
            (u'Torino, Italy', (42.23149050000001, 14.5476195)),
            (u'44037 Torino, Italy', (44.88877919999999, 11.9911579))
        ]
    }
]


class DummyGeoCoderResult(object):

    def __init__(self, data):
        self.address = data[0]
        self.latitude = data[1][0]
        self.longitude = data[1][1]


class DummyGeoCoder(GeoCoderUtility):

    def retrieve(self, address=None, google_api=None,
                 language=None):  # pylint: disable=W0613
        for item in test_params:
            if address == item['address']:
                return [DummyGeoCoderResult(res) for res in item['output']]
        raise GeocoderQueryError


class TestGeocoder(unittest.TestCase):
    layer = CGEO_MAPWIDGET_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.oid = self.portal.invokeFactory('Document', 'doc')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        self.obj = self.portal[self.oid]
        self.geo = getUtility(IGeoCoder)

    def test_geocoder_base(self):
        for item in test_params:
            locations = self.geo.retrieve(item['address'])
            self.assertEquals(
                [(loc.address, (loc.latitude, loc.longitude)) for loc in locations],
                item['output']
            )

    def test_geocoder_error(self):
        self.assertIsNone(self.geo.retrieve("not existent place aklhj asaas"))

    def test_geocoder_view(self):
        browser = Browser(self.layer['app'])
        browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,)
        )

        for item in test_params:
            obj_url = (
                "%s/@@geocoderview?address=%s" %
                (self.portal.absolute_url(), item['address'])
            )
            browser.open(obj_url)
            view_contents = json.loads(browser.contents)
            i = 0
            for place, (lat, lon) in view_contents:
                test_place, (test_lat, test_lon) = item['output'][i]
                self.assertEquals(test_place, place)
                self.assertEquals(test_lat, lat)
                self.assertEquals(test_lon, lon)
                i += 1


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGeocoder))
    return suite
