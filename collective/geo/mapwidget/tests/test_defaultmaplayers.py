import unittest2 as unittest

from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory

from zope.component import getUtility
from zope.component import queryUtility
from zope.component import getAdapters

from zope.publisher.browser import TestRequest

from ..interfaces import IDefaultMapLayers, IMapLayer
from ..testing import CGEO_MAPWIDGET_INTEGRATION


class TestDefaultMapLayers(unittest.TestCase):
    layer = CGEO_MAPWIDGET_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_utility(self):
        self.failUnless(queryUtility(IDefaultMapLayers))

    def _get_utility(self):
        utility = getUtility(IDefaultMapLayers)
        default_layers = [i[0] for i in self._get_registered_layers()]
        utility.geo_settings.default_layers = default_layers
        return utility

    def _get_registered_layers(self):
        return getAdapters((Interface,
                            Interface,
                            Interface,
                            Interface), IMapLayer)

    def test_layers_vocabulary(self):
        layer_ids = [i[0] for i in self._get_registered_layers()]
        vocab_util = queryUtility(IVocabularyFactory,
                        name='maplayersVocab')

        self.failUnless(vocab_util)

        vocab = vocab_util(self.portal)
        for item in vocab:
            self.assertIn(
                item.value,
                layer_ids,
                "term %s not in map layers" % item.value)

    def test_default_settings(self):
        layers = [u'osm', u'google_ter', u'google_hyb',
                  u'google_sat', u'google_map']
        utility = getUtility(IDefaultMapLayers)

        self.assertEquals(utility.geo_settings.default_layers, layers)

    def test_default_layers(self):
        layer_ids = [i[0] for i in self._get_registered_layers()]
        layers_utility = self._get_utility()
        layers = layers_utility.layers(None, None, None, None)
        self.assertEquals(len(layers), len(layer_ids))

    def test_select_layers_by_name(self):
        layer_ids = [i[0] for i in self._get_registered_layers()]
        layers_utility = self._get_utility()
        layers_utility.geo_settings.default_layers = layer_ids
        layers = layers_utility.layers(None, None, None, None)

        self.assertEquals(len(layers), len(layer_ids))

        for layer in layers:
            self.assertIn(
                layer.name,
                layer_ids,
                "%s not in map layers" % layer.name
            )

    def test_layer_protocols(self):
        """Test layers know what protocol is being used - HTTP or HTTPS."""
        layers_utility = self._get_utility()

        for protocol in ['https', 'http']:
            request = TestRequest(environ={'SERVER_URL':
                                           '%s://nohost' % protocol})

            self.assertEquals(request['SERVER_URL'], '%s://nohost' % protocol)

            layers = layers_utility.layers(None, request, None, None)
            for layer in layers:
                self.assertEquals(layer.protocol, protocol)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDefaultMapLayers))
    return suite
