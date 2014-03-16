import unittest2 as unittest
try:
    import json
except ImportError:
    import simplejson as json

from zope.interface import alsoProvides
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
            (
                u'Turin, Italy',
                (45.070562099999997, 7.6866186000000001)
            )
        ]
    },

    {
        'address': "Serravalle Italy",
        'output': [
            (
                u'Serravalle di Chienti Macerata, Italy',
                (43.075758700000002, 12.957291700000001)
            ),
            (
                u'46030 Serravalle a Po Mantua, Italy',
                (45.071769699999997, 11.0986653)
            ),
            (
                u'Serravalle, 50019 Sesto Fiorentino Florence, Italy',
                (43.847528799999999, 11.2683242)
            ),
            (
                u'Serravalle, 12026 Piasco Cuneo, Italy',
                (44.5675697, 7.4256900000000003)
            ),
            (
                u'Serravalle, 06046 Norcia Perugia, Italy',
                (42.785488399999998, 13.022334499999999)
            ),
            (
                u'Serravalle, 54023 Filattiera Massa-Carrara, Italy',
                (44.367425699999998, 9.9383029000000001)
            ),
            (
                u'Serravalle, Berra Ferrara, Italy',
                (44.967833300000002, 12.044703699999999)
            ),
            (
                u'Serravalle, Asti, Italy',
                (44.947478799999999, 8.1465417999999996)
            ),
            (
                u'Serravalle, Bibbiena Arezzo, Italy',
                (43.7736485, 11.8429064)
            ),
            (
                u'Serravalle, 38061 Ala Trento, Italy',
                (45.811786499999997, 11.0141562)
            )
        ]
    }
]


class DummyGeoCoderResult(object):

    def __init__(self, data):
        self.address = data[0]
        self.latitude = data[1][0]
        self.longitude = data[1][1]


class DummyGeoCoder(GeoCoderUtility):

    def retrieve(self, address=None, google_api=None):  # pylint: disable=W0613
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
                [(loc.address, (loc.latitude, loc.longitude))
                    for loc in locations],
                item['output']
            )

    def test_geocoder_error(self):
        self.assertRaises(GeocoderQueryError,
                          self.geo.retrieve,
                          "not existent place aklhj asaas")

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
