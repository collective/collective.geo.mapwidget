from zope.component import getUtility

from Products.CMFCore.Expression import Expression, getExprContext

from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.mapwidget import utils


_BINGURL = '%s://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6'
_GOOGLEURL = '%s://maps.google.com/maps/api/js?v=3.2&sensor=false'


class GeoSettingsView(object):
    """Geo Settings macros
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.layer_protocol = utils.getProtocolFromRequest(self.request)
        self.geosettings = getUtility(IRegistry).forInterface(IGeoSettings)

    @property
    def default_layers(self):
        return self.geosettings.default_layers

    @property
    def zoom(self):
        return  self.geosettings.zoom

    @property
    def map_center(self):
        return self.geosettings.longitude, self.geosettings.latitude

    @property
    def imgpath(self):
        return  self.geosettings.imgpath

    @property
    def googlemaps(self):
        for layer_id in self.default_layers:
            if layer_id.startswith('google'):
                return True
        return False

    @property
    def googleapi(self):
        return  self.geosettings.googleapi

    @property
    def google_maps_js(self):
        if self.googlemaps:
            #  google maps 3 api -- needs openlayer 2.10 version...
            return _GOOGLEURL % self.layer_protocol
        else:
            return None

    @property
    def bingapi(self):
        return  self.geosettings.bingapi

    @property
    def bingmaps(self):
        for layer_id in self.default_layers:
            if layer_id.startswith('bing'):
                return True
        return False

    @property
    def bing_maps_js(self):
        if self.bingmaps:
            return _BINGURL % self.layer_protocol
        else:
            return None

    @property
    def geo_setting_js(self):
        # Default configuration has been moved on mapwidgets
        # TODO: remove this property
        return None
