# import csv
# import cStringIO
# from zope.interface import implements

# from z3c.form import form, field, button

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
# from Products.CMFPlone.utils import getToolByName

# from plone.z3cform.layout import wrap_form
# from plone.z3cform.fieldsets import extensible, group

from z3c.form.interfaces import IWidget
from collective.geo.mapwidget.interfaces import IMapView
from collective.geo.mapwidget.browser.widget import MapWidget
from collective.geo.mapwidget.maplayers import MapLayer


class ShapeMapWidget(MapWidget):

    mapid = 'geoshapemap'
    _layers = ['shapeedit']

    @property
    def js(self):
        wkt_field_id = None
        if IWidget.providedBy(self.view):
            wkt_field_id = self.view.id
        elif getattr(self.view, 'widgets', None):
            wkt_field = self.view.widgets.get('wkt')
            if wkt_field:
                wkt_field_id = wkt_field.id

        if wkt_field_id:
            return """
  jq(window).bind('map-load', function(e, map) {
    var layer = map.getLayersByName('Edit')[0];
    var elctl = new OpenLayers.Control.WKTEditingToolbar(layer, {wktid: '%s'});
    map.addControl(elctl);
    elctl.activate();
  });""" % wkt_field_id


class ShapeEditLayer(MapLayer):

    name = 'shapeedit'

    jsfactory = """
    function() { return new OpenLayers.Layer.Vector('Edit');}
    """
