# -*- coding: utf-8 -*-
import urllib
from geopy import geocoders
from geopy.exc import GeocoderQueryError

from zope.interface import implements
from zope.schema import getFields
from zope.component import getUtility
from Products.CMFCore import DirectoryView

from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoFeatureStyle

from .interfaces import IGeoCoder


def get_feature_styles(context):
    fields = [i for i in getFields(IGeoFeatureStyle)]
    manager = IGeoFeatureStyle(context, None)
    use_custom_styles = getattr(manager, 'use_custom_styles', False)
    if not use_custom_styles:
        registry = getUtility(IRegistry)
        manager = registry.forInterface(IGeoFeatureStyle)
    styles = {
        'use_custom_styles': use_custom_styles
    }
    for name in fields:
        styles[name] = getattr(manager, name, None)

    return styles


def getProtocolFromRequest(request):
    """Determine which protocol layers should use for this request.

    Layers should, where possible, match the request protocol to avoid
    client browsers reporting errors to users.
    """
    server_url = request and request.get('SERVER_URL', '') or None
    return server_url and urllib.splittype(server_url)[0] or 'http'


def list_language_files():
    """ Returns a dictionary of available Openlayers translations.

    Keys are the language codes (lowercase, 2-4 in length).
    Values are the urls to the language files.
    """

    path = 'collective.geo.openlayers:skins/geo_openlayers/lang'
    urlbase = 'lang/'
    files = dict()

    info = DirectoryView._dirreg.getDirectoryInfo(path)

    if info:
        for key in info.getContents(DirectoryView._dirreg)[0].keys():
            files[key.replace('.js', '').lower()] = urlbase + key

    return files


def get_geocoder():
    return GeoCoderUtility()


class GeoCoderUtility(object):
    """Wrapper class for geopy
    """
    implements(IGeoCoder)

    def retrieve(self, address=None, google_api=None):
        # TODO: fix google_api > secret_key and client_id parameters
        # See https://github.com/geopy/geopy/blob/master/geopy/geocoders/googlev3.py#L31
        self.geocoder = geocoders.GoogleV3()

        if not address:
            raise GeocoderQueryError
        return self.geocoder.geocode(address, exactly_one=False)
