try:
    import json
except ImportError:
    import simplejson as json
from zope.component import getUtility
from Products.Five.browser import BrowserView
try:
    # geopy < 0.96
    from geopy.geocoders.googlev3 import GQueryError
    GeocoderQueryError = GQueryError
except ImportError:
    # geopy >= 0.96
    from geopy.exc import GeocoderQueryError

from ..interfaces import IGeoCoder


class GeoCoderView(BrowserView):
    """A simple view which provides a json output from geopy query.
    """

    def __init__(self, context, request):
        super(GeoCoderView, self).__init__(context, request)
        self.geocoder = getUtility(IGeoCoder)

    def __call__(self, address=None, google_api=None):
        try:
            locations = self.geocoder.retrieve(address, google_api)
        except GeocoderQueryError:
            return 'null'
        return json.dumps([loc for loc in locations])
