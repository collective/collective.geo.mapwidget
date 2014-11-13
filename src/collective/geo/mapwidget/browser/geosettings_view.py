from Acquisition import aq_inner
from zope.component import getUtility
from zope.component import getMultiAdapter
from Products.CMFCore.Expression import Expression, getExprContext

from plone.memoize import instance, view
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
        """Include google javascript only whether c.geo
        uses a google map layer and it isn't already
        included in the page
        """
        if not self.request.get('googlemaps_js'):
            for layer_id in self.default_layers:
                if layer_id.startswith('google'):
                    self.request.set('googlemaps_js', True)
                    return True
        return False

    @property
    def googleapi(self):
        return  self.geosettings.googleapi

    @property
    def google_maps_js(self):
        """return google maps 3 api javascript url
        """
        return _GOOGLEURL % self.layer_protocol

    @property
    def bingapi(self):
        return  self.geosettings.bingapi

    @property
    def bingmaps(self):
        """Include bing javascript only whether c.geo
        uses a bing map layer and it isn't already
        included in the page
        """
        if not self.request.get('bingmaps_js'):
            for layer_id in self.default_layers:
                if layer_id.startswith('bing'):
                    self.request.set('bingmaps_js', True)
                    return True
        return False

    @property
    def bing_maps_js(self):
        """return Bing maps javascript url
        """
        return _BINGURL % self.layer_protocol

    @property
    def location(self):
        try:
            location = self.context.getLocation()
        except AttributeError:
            return u''
        if isinstance(location, str):
            return location.decode('utf8')

    @property
    def localize(self):
        """ Returns True if the widget should be localized.
        """
        if self.request.get('openlayers_js') or self.language == 'en':
            return False

        self.request.set('openlayers_js', True)
        return self.language in self.language_files

    @property
    @view.memoize
    def language(self):
        """ Return the languagecode of the current context.
        """
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name="plone_portal_state")
        lang = aq_inner(self.context).Language() or \
            portal_state.default_language()

        return lang.lower()

    @property
    @instance.memoize
    def language_files(self):
        """Get, cache and return a list of openlayers language files.
        """
        return utils.list_language_files()

    @property
    def language_file(self, language=None):
        """ Returns the path to the openlayers language file of the
        given or the current language.
        """
        return self.language_files[language or self.language]

    @property
    def geo_setting_js(self):
        # Default configuration has been moved on mapwidgets
        # TODO: remove this property
        return None
