from Acquisition import aq_inner

from zope.publisher.browser import BrowserView

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize import instance, view

from collective.geo.mapwidget import utils

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

    @property
    def localize(self):
        """ Returns True if the widget should be localized.
        """
        if self.language == 'en':
            return False

        return self.language in self.language_files

    @property
    @view.memoize
    def language(self):
        """ Return the languagecode of the current context.
        """
        portal_state = self.context.unrestrictedTraverse("@@plone_portal_state")
        lang = aq_inner(self.context).Language() or portal_state.default_language()

        return lang.lower()

    @property
    @instance.memoize
    def language_files(self):
        """ Get, cache and return a list of openlayers language files.
        """
        return utils.list_language_files()

    @property
    def language_file(self, language=None):
        """ Returns the path to the openlayers language file of the
        given or the current language.
        """
        return self.language_files[language or self.language]

    @property
    def language_script(self):
        """ Returns the javscript call that sets the Openlayer langauge.
        """
        return "OpenLayers.Lang.setCode('%s');" % self.language
