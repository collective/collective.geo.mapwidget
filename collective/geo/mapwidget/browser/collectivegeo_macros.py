from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView

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
        geofeaturestyle = \
                self.context.restrictedTraverse('@@geofeaturestyle-view')
        for style in INLINE_STYLES:
            value = getattr(geofeaturestyle, INLINE_STYLES[style], None)
            if value:
                inline_css += "%s:%s;" % (style, value)

        return inline_css or None

    @property
    def location(self):
        try:
            location = self.context.getLocation()
        except AttributeError:
            return u''
        if isinstance(location, str):
            return location.decode('utf8')
