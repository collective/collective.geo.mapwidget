from zope.component import getUtility, queryAdapter

from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from collective.geo.settings.interfaces import IGeoFeatureStyle

MAP_STYLE_FIELDS = ['map_width', 'map_height']


class GeoFeatureStyleView(object):
    """Supporting Geo Feature Style settings used for maps
    """

    def __init__(self, context, request):
        """Initialise our feature style view with relevant map styles.

        If custom styles are specified for our context and they are enabled,
        then use them for styling our map. Otherwise, default to using the
        site-wide styles.
        """

        self.context = context
        self.request = request
        self.geofeaturestyle = None
        custom_styles = queryAdapter(self.context, IGeoCustomFeatureStyle)
        if custom_styles and custom_styles.use_custom_styles:
            self.geofeaturestyle = custom_styles
        else:
            self.geofeaturestyle = \
                    getUtility(IRegistry).forInterface(IGeoFeatureStyle)

    def __getattribute__(self, name):
        """Proxy attribute access to our local styles.

        If something has requested one of the fields in our custom styles
        then we get the property from there.  Otherwise, provide access
        normally using the parent method.
        """
        if name in MAP_STYLE_FIELDS:
            return getattr(self.geofeaturestyle, name, None)
        else:
            return super(GeoFeatureStyleView, self).__getattribute__(name)
