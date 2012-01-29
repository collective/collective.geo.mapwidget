from zope.component import getUtility

from Products.CMFCore.Expression import Expression, getExprContext

from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.mapwidget import utils


_YAHOOURL = 'http://api.maps.yahoo.com/ajaxymap?v=3.8&appid=%s'
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
    def yahoomaps(self):
        for layer_id in self.default_layers:
            if layer_id.startswith('yahoo'):
                return True
        return False

    @property
    def yahooapi(self):
        return  self.geosettings.yahooapi

    @property
    def yahoo_maps_js(self):
        if self.yahoomaps:
            #This API does not support SSL
            return _YAHOOURL % self.yahooapi
        else:
            return None

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
        lon, lat = self.map_center
        state = {'lon': lon,
                 'lat': lat,
                 'zoom': self.zoom}
        # set default configuration
        ret = ["cgmap.state = {'default': " \
            "{lon: %(lon)7f, lat: %(lat)7f, zoom: %(zoom)d }};" % state]
        # go through all maps in request and extract their state
        # to update map_state
        for mapid in self.request.get('cgmap_state_mapids', '').split():
            map_state = self.request.get('cgmap_state.%s' % mapid)
            state = {'mapid': mapid}
            for param in ('lon', 'lat', 'zoom',
                          'activebaselayer', 'activelayers'):
                val = map_state.get(param, None)
                state[param] = (val is not None) and ("'%s'" % val) or \
                                                                    'undefined'
            ret.append("cgmap.state['%(mapid)s'] = " \
                    "{lon: %(lon)s, lat: %(lat)s, zoom: %(zoom)s, " \
                    "activebaselayer: %(activebaselayer)s, activelayers: " \
                    "%(activelayers)s };" % state)

        # image path for change OpenLayers default images
        try:
            expr = Expression(str(self.imgpath))
            imgpath = expr(getExprContext(self.context))
        except:
            imgpath = ''

        #we portal_url to get geocoder view
        pstate = self.context.restrictedTraverse('plone_portal_state')
        portal_url = pstate.portal_url()
        ret.append("cgmap.portal_url = '%s';" % portal_url)

        ret.append("cgmap.imgpath = '%s';" % imgpath)
        return '\n'.join(ret)
