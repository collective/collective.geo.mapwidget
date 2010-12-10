from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView


class CollectiveGeoMacros(BrowserView):
    template = ViewPageTemplateFile('collectivegeo_macros.pt')

    def __getitem__(self, key):
        return self.template.macros[key]
