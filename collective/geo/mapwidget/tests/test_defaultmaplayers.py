import unittest

from zope.component import getUtility, queryUtility, getAdapters
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory
from zope.publisher.browser import TestRequest

from collective.geo.mapwidget.tests import base
from collective.geo.mapwidget.interfaces import IDefaultMapLayers, IMapLayer


class TestDefaultMapLayers(base.FunctionalTestCase):

    def test_utility(self):
        self.failUnless(queryUtility(IDefaultMapLayers))

    def _get_utility(self):
        utility = getUtility(IDefaultMapLayers)
        default_layers = [k for k, i in self._get_registered_layers()]
        utility.geo_settings.default_layers = default_layers
        return utility

    def _get_registered_layers(self):
        return getAdapters((Interface,
                            Interface,
                            Interface,
                            Interface), IMapLayer)

    def test_layers_vocabulary(self):
        default_layers = self._get_registered_layers()
        layer_ids = [k for k, i in default_layers]
        vocab_util = queryUtility(IVocabularyFactory,
                        name='maplayersVocab')

        self.failUnless(vocab_util)

        vocab = vocab_util(self.portal)
        for item in vocab:
            self.assertTrue(item.value in layer_ids,
                            "term %s not in map layers" % item.value)

    def test_default_settings(self):
        layers = [u'osm', u'google_ter', u'google_hyb',
                  u'google_sat', u'google_map']
        utility = getUtility(IDefaultMapLayers)

        self.assertEquals(utility.geo_settings.default_layers, layers)

    def test_default_layers(self):
        default_layers = self._get_registered_layers()
        layer_ids = [k for k, i in default_layers]
        layers_utility = self._get_utility()
        layers = layers_utility.layers(None, None, None, None)
        self.assertEquals(len(layers), len(layer_ids))

    def test_select_layers_by_name(self):
        default_layers = self._get_registered_layers()
        layer_ids = [k for k, i in default_layers][:3]
        layers_utility = self._get_utility()
        layers_utility.geo_settings.default_layers = layer_ids
        layers = layers_utility.layers(None, None, None, None)

        self.assertEquals(len(layers), len(layer_ids))

        for layer in layers:
            self.assertTrue(layer.name in layer_ids,
                            "%s not in map layers" % layer.name)

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
