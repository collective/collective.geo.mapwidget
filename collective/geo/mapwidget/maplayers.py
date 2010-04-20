"""
This module contains IMapLayer implementations for commonly available
base maps. These layers can be configured in the geo-settings control panel
or may be re-used in manually configured map-widgets.
"""
from zope.interface import implements
from collective.geo.mapwidget.interfaces import IMapLayer


class MapLayer(object):
    '''
    An empty IMapLayer implementation, useful as base class.

    MapLayers are named components specific for
    (view, request, context, widget).
    '''

    def __init__(self, view, request, context, widget):
        self.view = view
        self.request = request
        self.context = context
        self.widget = widget

    implements(IMapLayer)

    jsfactory = ""


class OSMMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "osm"

    jsfactory = """
    function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
        'http://tile.openstreetmap.org/',
        { 'type' : 'png',
          getURL: cgmap.osm_getTileURL,
          displayOutsideMaxExtent: true,
          attribution: '<a href="http://www.openstreetmap.org/">OpenStreetMap</a>'});}"""


class BingStreetMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "bmap"

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('Bing Streets',
        { 'type': VEMapStyle.Shaded,
          'sphericalMercator': true });}"""


class BingRoadsMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "brod"

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('Bing Roads',
        { 'type': VEMapStyle.Road,
          'sphericalMercator': true });}"""


class BingAerialMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "baer"

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('Bing Aerial',
        { 'type': VEMapStyle.Aerial,
          'sphericalMercator': true });}"""


class BingHybridMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "bhyb"

    jsfactory = """
    function() { return new OpenLayers.Layer.VirtualEarth('Bing Hybrid',
        { 'type': VEMapStyle.Hybrid,
          'sphericalMercator': true });}"""


class GoogleStreetMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "gmap"

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('Google',
        {'sphericalMercator': true});}"""


class GoogleSatelliteMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "gsat"

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('Satellite (Google)' ,
        {'type': G_SATELLITE_MAP, 'sphericalMercator': true});}"""


class GoogleHybridMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "ghyb"

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('Hybrid (Google)' ,
        {'type': G_HYBRID_MAP, 'sphericalMercator': true});}"""


class GoogleTerrainMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "gter"

    jsfactory = """
    function() { return new OpenLayers.Layer.Google('Terrain (Google)' ,
        {'type': G_PHYSICAL_MAP, 'sphericalMercator': true});}"""


class YahooStreetMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "ymap"

    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('Yahoo Street',
        {'type': YAHOO_MAP_REG, 'sphericalMercator': true});}"""


class YahooSatelliteMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "ysat"

    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('Yahoo Satellite',
        {'type': YAHOO_MAP_SAT, 'sphericalMercator': true});}"""


class YahooHybridMapLayer(MapLayer):

    def __init__(self, view=None, request=None, context=None, widget=None):
        pass

    name = "yhyb"

    jsfactory = """
    function() { return new OpenLayers.Layer.Yahoo('Yahoo Hybrid',
        {'type': YAHOO_MAP_HYB, 'sphericalMercator': true});}"""


from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoSettings
def defaultlayers():
    layers = []
    settings = getUtility(IRegistry).forInterface(IGeoSettings)
    # TODO: turn this into a Folder (or some sort of btree/dict storage), and manage layers as content objects in this folder
    # TODO: basically this tool imlpements the IMapLayers interface....
    #       shall we mark this out and make it really conform/adaptable to
    #       IMapLayers?
    layers = [OSMMapLayer()]
    if settings.googlemaps:
        layers.append(GoogleStreetMapLayer())
        layers.append(GoogleSatelliteMapLayer())
        layers.append(GoogleHybridMapLayer())
        layers.append(GoogleTerrainMapLayer())
    if settings.yahoomaps:
        layers.append(YahooStreetMapLayer())
        layers.append(YahooSatelliteMapLayer())
        layers.append(YahooHybridMapLayer())
    if settings.bingmaps:
        layers.append(BingStreetMapLayer())
        layers.append(BingRoadsMapLayer())
        layers.append(BingAerialMapLayer())
        layers.append(BingHybridMapLayer())
    return layers
