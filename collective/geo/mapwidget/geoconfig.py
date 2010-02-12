from persistent import Persistent
from zope.interface import implements
from zope.component import getUtility

from collective.geo.mapwidget.interfaces import IGeoSettings
from collective.geo.mapwidget.maplayers import (OSMMapLayer, BingStreetMapLayer, BingRoadsMapLayer,
                                               BingAerialMapLayer, BingHybridMapLayer,
                                               GoogleStreetMapLayer, GoogleSatelliteMapLayer,
                                               GoogleHybridMapLayer, GoogleTerrainMapLayer,
                                               YahooStreetMapLayer, YahooSatelliteMapLayer,
                                               YahooHybridMapLayer)


class GeoSettings(Persistent):
    """
        GeoSettings have some propreties. We can get its propterties directly
        >>> config = GeoSettings()
        >>> config.zoom
        10.0

        or by the 'get' method
        >>> config.get('googlemaps')
        True

        we can set GeoSettins in this way
        >>> config.zoom = 9.5
        >>> config.zoom
        9.5

        or by the 'set' method
        >>> config.set('zoom', 10.0)
        >>> config.zoom
        10.0

        return False for unknown properties
        >>> config.get('notthere')
        False

        check whether the tool returns only activated layers.
        if all layers are turned off, there should be at least the osm layer there
        >>> config.googlemaps = False
        >>> len(config.layers)
        1
        >>> config.layers[0].name
        'osm'

        turn on yahoo and bing
        >>> config.yahoomaps = True
        >>> config.bingmaps = True
        >>> len(config.layers)
        8

        turn on all layers, the first layer is osm
        >>> config.googlemaps = True
        >>> len(config.layers)
        12
        >>> config.layers[0].name
        'osm'

    """
    implements(IGeoSettings)

    latitude = 45.682143
    longitude = 7.68047
    zoom = 10.0
    googlemaps = True # key works only for localhost?
    googleapi = 'ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw'

    yahoomaps = False # turned off by default because it needs API key
    yahooapi = 'YOUR_API_KEY'

    bingmaps = False

    # TODO: turn this into a Folder (or some sort of btree/dict storage), and manage layers as content objects in this folder
    # TODO: basically this tool imlpements the IMapLayers interface....
    #       shall we mark this out and make it really conform/adaptable to
    #       IMapLayers?
    @property
    def layers(self):
        layers = [OSMMapLayer()]
        if self.googlemaps:
            layers.append(GoogleStreetMapLayer())
            layers.append(GoogleSatelliteMapLayer())
            layers.append(GoogleHybridMapLayer())
            layers.append(GoogleTerrainMapLayer())
        if self.yahoomaps:
            layers.append(YahooStreetMapLayer())
            layers.append(YahooSatelliteMapLayer())
            layers.append(YahooHybridMapLayer())
        if self.bingmaps:
            layers.append(BingStreetMapLayer())
            layers.append(BingRoadsMapLayer())
            layers.append(BingAerialMapLayer())
            layers.append(BingHybridMapLayer())
        return layers

    def set(self, key, val):
        return self.__setattr__(key, val)

    def get(self, key, default=False):
        try:
            return self.__getattribute__(key)
        except:
            return default


class GeoConfig(object):
    """
        Non ho ancora capito a cosa serva sto coso
        We get the IGeoSettings utility
        >>> config = GeoConfig()
        >>> config.getSettings()
        <class 'collective.geo.mapwidget.geoconfig.GeoSettings'>

        and its properties
        >>> config.getSettings().zoom
        10.0

    """

    def getSettings(self):
        return getUtility(IGeoSettings)
