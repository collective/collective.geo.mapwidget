from z3c.form import field, form, subform, button
from z3c.form.interfaces import IFormLayer
from plone.z3cform import z2
from plone.z3cform.fieldsets import extensible

from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import implements
from zope.component import getUtility
from zope.app.pagetemplate import viewpagetemplatefile
from zope.app.component.hooks import getSite

from collective.geo.mapwidget.interfaces import IGeoSettings, IMapView
from collective.geo.mapwidget import GeoMapwidgetMessageFactory as _
from collective.geo.mapwidget.browser.widget import MapWidget, MapLayer


def geo_settings(context):
    return getUtility(IGeoSettings)


def back_to_controlpanel(self):
    root = getSite()
    return dict(url=root.absolute_url() + '/plone_control_panel')


class GeopointForm(subform.EditSubForm):
    template = viewpagetemplatefile.ViewPageTemplateFile('geopointform.pt')

    implements(IMapView)

    fields = field.Fields(IGeoSettings).select('longitude', 'latitude')

    mapfields = ['geosettings-cgmap']

    def update(self):
        self.updateWidgets()


class GeoControlpanelForm(extensible.ExtensibleForm, form.EditForm):
    template = viewpagetemplatefile.ViewPageTemplateFile(
                                            'form-with-subforms.pt')

    fields = field.Fields(IGeoSettings).select('zoom',
                                               'googlemaps',
                                               'googleapi',
                                               'yahoomaps',
                                               'yahooapi',
                                               'bingmaps')

    default_fieldset_label = _(u"Base settings")

    heading = _(u'Configure Collective Geo Settings')

    @property
    def css_class(self):
        return "subform openlayers-level-%s" % self.level

    level = 1

    def __init__(self, context, request):
        super(GeoControlpanelForm, self).__init__(context, request)
        subform = GeopointForm(self.context, self.request, self)
        subform.level = self.level + 1

        self.subforms = [subform, ]

    def update(self):
        # update subforms first, else the values won't
        # be available in button handler
        for subform in self.subforms:
            subform.update()
        super(GeoControlpanelForm, self).update()

    def updateWidgets(self):
        super(GeoControlpanelForm, self).updateWidgets()
        self.widgets['googleapi'].size = 80
        self.widgets['yahooapi'].size = 80

    @button.handler(form.EditForm.buttons['apply'])
    def handle_add(self, action):
        subdata, suberrors = self.subforms[0].extractData()
        data, errors = self.extractData()
        if errors or suberrors:
            return

        utility = IGeoSettings(self.context)
        for key, val in data.items():
            utility.set(key, val)

        for key, val in subdata.items():
            utility.set(key, val)


class GeoControlpanel(BrowserView):

    __call__ = ViewPageTemplateFile('controlpanel.pt')

    label = _(u'Geo Settings')
    description = _(u"Collective Geo Default Settings")
    back_link = back_to_controlpanel

    request_layer = IFormLayer
    form = GeoControlpanelForm

    # NOTE: init code taken from plone.z3cform FormWrapper...
    #       maybe extending FormWrapper would be an option?
    def __init__(self, context, request):
        super(GeoControlpanel, self).__init__(context, request)
        if self.form is not None:
            self.form_instance = self.form(aq_inner(self.context),
                                                        self.request)
            self.form_instance.__name__ = self.__name__

    def contents(self):
        z2.switch_on(self)
        self.form_instance.update()
        return self.form_instance.render()


class ControlPanelMapWidget(MapWidget):

    mapid = 'geosettings-cgmap'
    style = "height:450px; width:450px;"

    _layers = ['markeredit']

    def __init__(self, view, request, context):
        super(ControlPanelMapWidget, self).__init__(view, request, context)
        self.lonid = view.widgets['longitude'].id
        self.latid = view.widgets['latitude'].id
        self.zoomid = view.__parent__.widgets['zoom'].id

    @property
    def js(self):
        return """
    jq(window).load(function() {
      var map = cgmap.config['geosettings-cgmap'].map;
      var layer = map.getLayersByName('Marker')[0];
      var elctl = new OpenLayers.Control.MarkerEditingToolbar(layer,
                                {lonid: '%s', latid: '%s', zoomid: '%s'});
      map.addControl(elctl);
      elctl.activate();
    });
""" % (self.lonid, self.latid, self.zoomid)


class MarkerEditLayer(MapLayer):

    name = "markeredit"

    jsfactory = """
    function() { return new OpenLayers.Layer.Vector('Marker',
                                    {renderOptions: {yOrdering: true}});}
    """
