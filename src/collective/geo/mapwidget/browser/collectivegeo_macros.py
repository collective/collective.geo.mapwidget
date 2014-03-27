from zope.component import getMultiAdapter
from zope.publisher.browser import BrowserView

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

INLINE_STYLES = {'width': 'map_width',
                 'height': 'map_height'}


class CollectiveGeoMacros(BrowserView):
    template = ViewPageTemplateFile('collectivegeo_macros.pt')

    def __getitem__(self, key):
        return self.template.macros[key]

    def map_inline_css(self):
        """Return inline CSS for our map according to style settings.
        """
        inline_css = ''
        geofeaturestyle = getMultiAdapter(
            (self.context, self.request),
            name='geofeaturestyle-view'
        )
        for style in INLINE_STYLES:
            value = getattr(geofeaturestyle, INLINE_STYLES[style], None)
            if value:
                inline_css += "%s:%s;" % (style, value)

        return inline_css or None
