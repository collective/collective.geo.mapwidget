"""
This module contains IMapLayer implementations for commonly available
base maps. These layers can be configured in the geo-settings control panel
or may be re-used in manually configured map-widgets.
"""
from zope.interface import implements
from zope.component import getUtility, queryMultiAdapter

from plone.registry.interfaces import IRegistry

from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.mapwidget.interfaces import IMapLayer
from collective.geo.mapwidget.interfaces import IDefaultMapLayers

from collective.geo.mapwidget import GeoMapwidgetMessageFactory as _


class MapLayer(object):
    '''
    An empty IMapLayer implementation, useful as base class.

    MapLayers are named components specific for
    (view, request, context, widget).
    '''

    implements(IMapLayer)
    jsfactory = u""
    Title = u""
    # we need a property to evaluate if the layer map is based on google,
    # bing or yahoo maps to include a external javascrpt
    type = 'base'

    def __init__(self, view=None, request=None, context=None, widget=None):
        self.view = view
        self.request = request
        self.context = context
        self.widget = widget


class OSMMapLayer(MapLayer):

    name = u"osm"
    Title = _(u"OpenStreetMap")

    jsfactory = u"""
    function() { return new OpenLayers.Layer.TMS( '%s',
        'http://tile.openstreetmap.org/',
        { 'type' : 'png',
          getURL: cgmap.osm_getTileURL,
          displayOutsideMaxExtent: true,
          numZoomLevels: 19,
          attribution: '<a href="http://www.openstreetmap.org/">OpenStreetMap</a>'});}""" % Title


class BingStreetMapLayer(MapLayer):

    name = u"bing_map"
    Title = _(u"Bing Streets")
    type = 'bing'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.VirtualEarth('%s',
        { 'type': VEMapStyle.Shaded,
          'sphericalMercator': true });}""" % Title


class BingRoadsMapLayer(MapLayer):

    name = u"bing_rod"
    Title = _(u"Bing Roads")
    type = 'bing'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.VirtualEarth('%s',
        { 'type': VEMapStyle.Road,
          'sphericalMercator': true });}""" % Title


class BingAerialMapLayer(MapLayer):

    name = u"bing_aer"
    Title = _(u"Bing Aerial")
    type = 'bing'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.VirtualEarth('%s',
        { 'type': VEMapStyle.Aerial,
          'sphericalMercator': true });}""" % Title


class BingHybridMapLayer(MapLayer):

    name = u"bing_hyb"
    Title = _(u"Bing Hybrid")
    type = 'bing'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.VirtualEarth('%s',
        { 'type': VEMapStyle.Hybrid,
          'sphericalMercator': true });}""" % Title


class GoogleStreetMapLayer(MapLayer):

    name = u"google_map"
    Title = _(u"Google")
    type = 'google'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.Google('%s',
        {'sphericalMercator': true, numZoomLevels: 20});}""" % Title


class GoogleSatelliteMapLayer(MapLayer):

    name = u"google_sat"
    Title = _(u"Satellite (Google)")
    type = 'google'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.Google('%s' ,
        {'type': google.maps.MapTypeId.SATELLITE, numZoomLevels: 22,
         'sphericalMercator': true});}""" % Title


class GoogleHybridMapLayer(MapLayer):

    name = u"google_hyb"
    Title = _(u"Hybrid (Google)")
    type = 'google'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.Google('%s' ,
        {'type': google.maps.MapTypeId.HYBRID, numZoomLevels: 20,
         'sphericalMercator': true});}""" % Title


class GoogleTerrainMapLayer(MapLayer):

    name = u"google_ter"
    Title = _(u"Terrain (Google)")
    type = 'google'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.Google('%s' ,
        {'type': google.maps.MapTypeId.TERRAIN,  numZoomLevels: 20,
         'sphericalMercator': true});}""" % Title


class YahooStreetMapLayer(MapLayer):

    name = u"yahoo_map"
    Title = _(u"Yahoo Street")
    type = 'yahoo'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.Yahoo('%s',
        {'type': YAHOO_MAP_REG, 'sphericalMercator': true});}""" % Title


class YahooSatelliteMapLayer(MapLayer):

    name = u"yahoo_sat"
    Title = _(u"Yahoo Satellite")
    type = 'yahoo'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.Yahoo('%s',
        {'type': YAHOO_MAP_SAT, 'sphericalMercator': true});}""" % Title


class YahooHybridMapLayer(MapLayer):

    name = u"yahoo_hyb"
    Title = _(u"Yahoo Hybrid")
    type = 'yahoo'

    jsfactory = u"""
    function() { return new OpenLayers.Layer.Yahoo('%s',
        {'type': YAHOO_MAP_HYB, 'sphericalMercator': true});}""" % Title


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
            layer = queryMultiAdapter((None, None, None, None),
                                                    IMapLayer, name=layerid)
            if layer:
                layers.append(layer)

        return layers
