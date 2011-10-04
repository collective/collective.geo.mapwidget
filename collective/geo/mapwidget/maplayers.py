"""
This module contains IMapLayer implementations for commonly available
base maps. These layers can be configured in the geo-settings control panel
or may be re-used in manually configured map-widgets.
"""
from zope.interface import implements
from zope.component import getUtility, queryMultiAdapter

from plone.registry.interfaces import IRegistry
from plone.memoize.instance import memoizedproperty

from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.mapwidget.interfaces import IMapLayer
from collective.geo.mapwidget.interfaces import IDefaultMapLayers

from collective.geo.mapwidget import GeoMapwidgetMessageFactory as _
from collective.geo.mapwidget import utils


class MapLayer(object):
    '''
    An empty IMapLayer implementation, useful as base class.

    MapLayers are named components specific for
    (view, request, context, widget).
    '''

    implements(IMapLayer)
    Title = u""
    name = u""
    # we need a property to evaluate if the layer map is based on google,
    # bing or yahoo maps to include a external javascrpt
    type = 'base'

    def __init__(self, view=None, request=None, context=None, widget=None):
        self.view = view
        self.request = request
        self.protocol = utils.getProtocolFromRequest(self.request)
        self.context = context
        self.widget = widget

    @memoizedproperty
    def jsfactory(self):
        try:
            template = self.context.restrictedTraverse(
                                    str('%s-layer' % self.name))
        except AttributeError:
            return u""
        return template() % dict(title=self.Title, protocol=self.protocol)


class OSMMapLayer(MapLayer):
    name = u"osm"
    Title = _(u"OpenStreetMap")


class BingStreetMapLayer(MapLayer):
    name = u"bing_map"
    Title = _(u"Bing Streets")
    type = 'bing'


class BingRoadsMapLayer(MapLayer):
    name = u"bing_rod"
    Title = _(u"Bing Roads")
    type = 'bing'


class BingAerialMapLayer(MapLayer):
    name = u"bing_aer"
    Title = _(u"Bing Aerial")
    type = 'bing'


class BingHybridMapLayer(MapLayer):
    name = u"bing_hyb"
    Title = _(u"Bing Hybrid")
    type = 'bing'


class GoogleStreetMapLayer(MapLayer):
    name = u"google_map"
    Title = _(u"Google")
    type = 'google'


class GoogleSatelliteMapLayer(MapLayer):
    name = u"google_sat"
    Title = _(u"Satellite (Google)")
    type = 'google'


class GoogleHybridMapLayer(MapLayer):
    name = u"google_hyb"
    Title = _(u"Hybrid (Google)")
    type = 'google'


class GoogleTerrainMapLayer(MapLayer):
    name = u"google_ter"
    Title = _(u"Terrain (Google)")
    type = 'google'


class YahooStreetMapLayer(MapLayer):
    name = u"yahoo_map"
    Title = _(u"Yahoo Street")
    type = 'yahoo'


class YahooSatelliteMapLayer(MapLayer):
    name = u"yahoo_sat"
    Title = _(u"Yahoo Satellite")
    type = 'yahoo'


class YahooHybridMapLayer(MapLayer):
    name = u"yahoo_hyb"
    Title = _(u"Yahoo Hybrid")
    type = 'yahoo'


class DefaultMapLayers(object):
    """Utility to store default map layers
    """

    implements(IDefaultMapLayers)

    @property
    def geo_settings(self):
        return getUtility(IRegistry).forInterface(IGeoSettings)

    @property
    def default_layers(self):
        return (u'osm', )

    def layers(self, view, request, context, widget):
        default_layers = self.geo_settings.default_layers
        if not default_layers:
            default_layers = self.default_layers

        layers = []
        for layerid in default_layers:
            layer = queryMultiAdapter((view, request, context, widget),
                                                    IMapLayer, name=layerid)
            if layer:
                layers.append(layer)

        return layers
