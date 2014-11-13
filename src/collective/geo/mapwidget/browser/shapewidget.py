from z3c.form.interfaces import IWidget
from collective.geo.mapwidget.interfaces import IMapView
from collective.geo.mapwidget.browser.widget import MapWidget
from collective.geo.mapwidget.maplayers import MapLayer


class ShapeMapWidget(MapWidget):

    mapid = 'geoshapemap'

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
(function ($) {
    $(window).load(function() {
        // collective geo edit map
        $('#%s').collectivegeo(
            'add_edit_layer',
            '%s'
        );
        $('#%s').collectivegeo('add_geocoder');
    });
}(jQuery));
""" % (self.mapid, wkt_field_id)
