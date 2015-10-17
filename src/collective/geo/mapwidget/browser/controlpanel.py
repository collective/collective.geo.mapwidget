# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.geo.mapwidget import GeoMapwidgetMessageFactory as _
from collective.geo.mapwidget.browser.widget import MapWidget
from collective.geo.mapwidget.interfaces import IMapView
from collective.geo.settings.events import GeoSettingsEvent
from collective.geo.settings.interfaces import IGeoSettings, IGeoFeatureStyle
from collective.z3cform.colorpicker.colorpickeralpha import \
    ColorpickerAlphaFieldWidget
from plone.z3cform.fieldsets import extensible, group
from plone.z3cform.layout import FormWrapper
from z3c.form import field, form, subform, button
from zope.event import notify
from zope.interface import implements
from zope.schema import Choice


def back_to_controlpanel(context):
    portal_url = context.restrictedTraverse('plone_portal_state').portal_url()
    return dict(url='%s/plone_control_panel' % portal_url)


class GeopointForm(subform.EditSubForm):
    heading = _(u"Default map position")
    contents_top = _(
        u"Set the centre point and the zoom level of the map "
        u"used when the system cannot use any other point to center the map "
        u"(e.g. when displaying the map "
        u"to georeference an item for the first time)")
    template = ViewPageTemplateFile('geopointform.pt')
    implements(IMapView)
    fields = field.Fields(IGeoSettings).select('longitude', 'latitude',
                                               'zoom')
    mapfields = ['geosettings-cgmap']

    def update(self):
        self.updateWidgets()

    def applyChanges(self, data):
        content = self.getContent()
        return form.applyChanges(self, content, data)


class GeoStylesGroup(group.Group):

    label = _(u"Style")
    description = _(u"Set default styles for geographical shapes")

    @property
    def fields(self):
        fields = field.Fields(IGeoFeatureStyle).select('marker_image')
        fields += field.Fields(IGeoSettings).select('imgpath')
        fields += field.Fields(IGeoFeatureStyle).select(
            'marker_image_size',
            'map_width',
            'linecolor',
            'map_height',
            'polygoncolor',
            'display_properties',
            'linewidth',
        )
        fields['linecolor'].widgetFactory = ColorpickerAlphaFieldWidget
        fields['polygoncolor'].widgetFactory = ColorpickerAlphaFieldWidget
        return fields


class GeoAdvancedConfGroup(group.Group):

    label = _(u"Advanced")
    description = _(u"Advanced configurations")

    fields = field.Fields(IGeoSettings).select('map_viewlet_managers')

    def updateWidgets(self):
        super(GeoAdvancedConfGroup, self).updateWidgets()
        widgets = ('googleapi', 'bingapi')
        for w in self.widgets:
            if w in widgets:
                self.widgets[w].size = 80
                self.widgets[w].update()


def control_panel_fields():
    form_fields = field.Fields(IGeoSettings).select(
        'default_layers', 'bingapi')
    form_fields += field.Fields(IGeoFeatureStyle).select(
        'map_viewlet_position')
    default_layer_field = form_fields['default_layers']
    default_layer_field.field.value_type = Choice(
        title=_(u"Layers"),
        source="maplayersVocab"
    )
    return form_fields


class GeoControlpanelForm(extensible.ExtensibleForm, form.EditForm):

    # This is a copy of plone/app/z3cform/templates/macros.pt plus subforms
    template = ViewPageTemplateFile('form-with-subforms.pt')
    form.extends(form.EditForm, ignoreButtons=True)

    default_fieldset_label = _(u"Base settings")

    heading = _(u'Configure Collective Geo Settings')
    fields = control_panel_fields()
    groups = (GeoStylesGroup, GeoAdvancedConfGroup)
    label = _(u'Geo Settings')
    form_name = _(u"Configure element")
    description = _(u"Collective Geo Default Settings")

    level = 1

    @property
    def css_class(self):
        return "subform openlayers-level-%s" % self.level

    def __init__(self, context, request):
        super(GeoControlpanelForm, self).__init__(context, request)
        _subform = GeopointForm(self.context, self.request, self)
        self.ptool = getToolByName(self.context, 'plone_utils')
        _subform.level = self.level + 1

        self.subforms = [_subform, ]

    def update(self):
        # update subforms first, else the values won't
        # be available in button handler
        for _subform in self.subforms:
            _subform.update()
        super(GeoControlpanelForm, self).update()

    @button.buttonAndHandler(_(u'Apply'), name='apply')
    def handle_apply(self, action):
        subdata, suberrors = self.subforms[0].extractData()
        data, errors = self.extractData()

        if errors or suberrors:
            self.status = self.formErrorsMessage
            return

        changes = self.applyChanges(data)
        coordinate_changes = self.subforms[0].applyChanges(subdata)
        if changes or coordinate_changes:
            self.status = self.successMessage
            notify(GeoSettingsEvent(self.context, data))
        else:
            self.status = self.noChangesMessage

        self.ptool.addPortalMessage(self.status, 'info')
        self.request.response.redirect(self.back_link)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handle_cancel(self, action):
        self.ptool.addPortalMessage(self.noChangesMessage, 'info')
        self.request.response.redirect(self.back_link)

    @property
    def back_link(self):
        return back_to_controlpanel(self.context)['url']


class GeoControlpanel(FormWrapper):

    index = ViewPageTemplateFile('controlpanel.pt')
    form = GeoControlpanelForm


class ControlPanelMapWidget(MapWidget):

    mapid = 'geosettings-cgmap'

    @property
    def js(self):
        return None
