try:
    import json
except ImportError:
    import simplejson as json
from zope.component import getUtility, getMultiAdapter
from Products.Five.browser import BrowserView
from geopy.exc import GeocoderQueryError

from ..interfaces import IGeoCoder


class GeoCoderView(BrowserView):
    """A simple view which provides a json output from geopy query.
    """

    def __init__(self, context, request):
        super(GeoCoderView, self).__init__(context, request)
        self.geocoder = getUtility(IGeoCoder)

    def __call__(self, address=None, google_api=None):
        context = self.context.aq_inner
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        language = portal_state.language()

        try:
            locations = self.geocoder.retrieve(address, google_api, language)
        except GeocoderQueryError:
            return 'null'

        if not locations:
            return 'null'

        return json.dumps(
            [(loc.address, (loc.latitude, loc.longitude)) for loc in locations]
        )
