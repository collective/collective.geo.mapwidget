"""
This module contains IMapLayer implementations for commonly available
base maps. These layers can be configured in the geo-settings control panel
or may be re-used in manually configured map-widgets.
"""
from zope.interface import implements
from zope.component import getUtility, getAdapters

from plone.registry.interfaces import IRegistry

from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.mapwidget.interfaces import IMapLayer
from collective.geo.mapwidget.interfaces import IDefaultMapLayers

from zope.interface import Interface
from zope.publisher.interfaces.http import IHTTPRequest
from collective.geo.mapwidget.interfaces import IMapWidget

from collective.geo.mapwidget import GeoMapwidgetMessageFactory as _


class MapLayer(object):
    '''
    An empty IMapLayer implementation, useful as base class.

    MapLayers are named components specific for
    (view, request, context, widget).
    '''

    implements(IMapLayer)
    jsfactory = ""
    title = u""

    def __init__(self, view=None, request=None, context=None, widget=None):
        self.view = view
        self.request = request
        self.context = context
        self.widget = widget


class OSMMapLayer(MapLayer):

    name = "osm"
    title = _(u"OpenStreetMap")

    jsfactory = """
    function() { return new OpenLayers.Layer.TMS( '%s',
        'http://tile.openstreetmap.org/',
        { 'type' : 'png',
          getURL: cgmap.osm_getTileURL,
          displayOutsideMaxExtent: true,
          attribution: '<a href="http://www.openstreetmap.org/">OpenStreetMap</a>'});}""" % title


class BingStreetMapLayer(MapLayer):

    name = "bmap"
    title = _(u"Bing Streets")

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('%s',
        { 'type': VEMapStyle.Shaded,
          'sphericalMercator': true });}""" % title


class BingRoadsMapLayer(MapLayer):

    name = "brod"
    title = _(u"Bing Roads")

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('%s',
        { 'type': VEMapStyle.Road,
          'sphericalMercator': true });}""" % title


class BingAerialMapLayer(MapLayer):

    name = "baer"
    title = _(u"Bing Aerial")

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('%s',
        { 'type': VEMapStyle.Aerial,
          'sphericalMercator': true });}""" % title


class BingHybridMapLayer(MapLayer):

    name = "bhyb"
    title = _(u"Bing Hybrid")

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('%s',
        { 'type': VEMapStyle.Hybrid,
          'sphericalMercator': true });}""" % title


class GoogleStreetMapLayer(MapLayer):

    name = "gmap"
    title = _(u"Google")

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('%s',
        {'sphericalMercator': true});}""" % title


class GoogleSatelliteMapLayer(MapLayer):

    name = "gsat"
    title = _(u"Satellite (Google)")

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('%s' ,
        {'type': G_SATELLITE_MAP, 'sphericalMercator': true});}""" % title


class GoogleHybridMapLayer(MapLayer):

    name = "ghyb"
    title = _(u"Hybrid (Google)")

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('%s' ,
        {'type': G_HYBRID_MAP, 'sphericalMercator': true});}""" % title


class GoogleTerrainMapLayer(MapLayer):

    name = "gter"
    title = _(u"Terrain (Google)")

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('%s' ,
        {'type': G_PHYSICAL_MAP, 'sphericalMercator': true});}""" % title


class YahooStreetMapLayer(MapLayer):

    name = "ymap"
    title = _(u"Yahoo Street")

    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('%s',
        {'type': YAHOO_MAP_REG, 'sphericalMercator': true});}""" % title


class YahooSatelliteMapLayer(MapLayer):

    name = "ysat"
    title = _(u"Yahoo Satellite")
    
    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('%s',
        {'type': YAHOO_MAP_SAT, 'sphericalMercator': true});}""" % title


class YahooHybridMapLayer(MapLayer):

    name = "yhyb"
    title = _(u"Yahoo Hybrid")

    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('%s',
        {'type': YAHOO_MAP_HYB, 'sphericalMercator': true});}""" % title


class DefaultMapLayers(object):
    """Utility to store default map layers
    """

    implements(IDefaultMapLayers)

    @property
    def geo_settings(self):
        return getUtility(IRegistry).forInterface(IGeoSettings)

    def layers(self):
        # getAdapters((Interface, IHTTPRequest, Interface, IMapWidget), IMapLayer)
        # from zope.component import getMultiAdapter
        # getMultiAdapter((self.view, self.request, self.context, self.widget), IMapLayer, name=layerid)
        # pippo = [k for k, v in getAdapters((Interface, IHTTPRequest, Interface, IMapWidget), IMapLayer)

        layers = [OSMMapLayer()]
        if self.geo_settings.googlemaps:
            layers.append(GoogleStreetMapLayer())
            layers.append(GoogleSatelliteMapLayer())
            layers.append(GoogleHybridMapLayer())
            layers.append(GoogleTerrainMapLayer())
        if self.geo_settings.yahoomaps:
            layers.append(YahooStreetMapLayer())
            layers.append(YahooSatelliteMapLayer())
            layers.append(YahooHybridMapLayer())
        if self.geo_settings.bingmaps:
            layers.append(BingStreetMapLayer())
            layers.append(BingRoadsMapLayer())
            layers.append(BingAerialMapLayer())
            layers.append(BingHybridMapLayer())
        return layers
