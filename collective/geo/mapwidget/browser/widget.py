
from zope.interface import implements
from zope.component import getMultiAdapter, getUtility
from zope.publisher.interfaces.browser import IBrowserView

from Products.Five import BrowserView

from collective.geo.mapwidget.interfaces import (IMaps, IMapWidget, IMapLayer,
                                                IMapLayers, IMapView,
                                                IDefaultMapLayers)


class MapView(BrowserView):
    '''
    Helper view to look up mapwidgets for current view and context.
    '''
    # TODO: shall this be a IMapView or the view itself?
    implements(IMapView)

    def mapwidgets(self):
        if IBrowserView.providedBy(self.context):
            return getMultiAdapter((self.context, self.request,
                                        self.context.context), IMaps)
        return []


class MapWidgets(list):
    '''IMaps adapter which initialises IMapWidgets
    for current view ad context.
    '''
# TODO: ensure all these methods are available
#    def __getitem__(key):
#         """Get a value for a key
#
#         A KeyError is raised if there is no value for the key.
#         """
#
#     def get(key, default=None):
#         """Get a value for a key
#
#         The default is returned if there is no value for the key.
#         """
#
#     def __contains__(key):
#         """Tell if a key exists in the mapping."""
#
# def keys():
#         """Return the keys of the mapping object.
#         """
#
#
#     def __iter__():
#         """Return an iterator for the keys of the mapping object.
#         """
#
#     def values():
#         """Return the values of the mapping object.
#         """
#
#     def items():
#         """Return the items of the mapping object.
#         """
#
#     def __len__():
#         """Return the number of items.
#         """

    implements(IMaps)

    def __init__(self, view, request, context):
        self.keys = {}
        self.view = view
        self.request = request
        self.context = context
        mapfields = getattr(view, 'mapfields', None)
        if mapfields:
            for mapid in mapfields:
                if IMapWidget.providedBy(mapid):
                    # is already a MapWidget, just take it
                    self.__append(mapid.mapid, mapid)
                elif isinstance(mapid, basestring):
                    # is only a name... lookup the widget
                    self.__append(mapid,
                                  getMultiAdapter((self.view, self.request,
                                                                self.context),
                                                  IMapWidget,
                                                  name=mapid))
                else:
                    raise ValueError("Can't create IMapWidget for %s"\
                                                               % repr(mapid))
        else:
            # there are no mapfields let's look up the default widget
            self.__append('default-cgmap',
                          getMultiAdapter((self.view, self.request,
                                                          self.context),
                                          IMapWidget,
                                          name='default-cgmap'))

    def __append(self, key, value):
        self.keys[key] = value
        self.append(value)

    def __getitem__(self, key):
        if isinstance(key, basestring):
            return self.keys[key]
        return super(MapWidgets, self).__getitem__(key)


class MapWidget(object):
    '''The default IMapWidget, which also can serve as handy base class.
    '''

    implements(IMapWidget)

    mapid = 'default-cgmap'
    klass = 'widget-cgmap'
    js = "// default"
    _layers = []

    def __init__(self, view, request, context):
        self.view = view
        self.request = request
        self.context = context

    @property
    def layers(self):
        return getMultiAdapter((self.view, self.request, self.context, self),
                                                                    IMapLayers)

    def addClass(self, klass):
        if not self.klass:
            self.klass = unicode(klass)
        else:
            # Make sure items are not repeated.
            parts = self.klass.split() + [unicode(klass)]
            self.klass = u' '.join(frozenset(parts))


class MapLayers(dict):
    '''
    The default IMapLayers implementation.

    Checks geo settings tool for enabled layers and adds them
    if enabled (widget.usedefault).

    TODO: this impl is too tigly copled with the default MapWigdet
          implementation.
          esp.: it should not look for widget._layers attribute.
    '''

    implements(IMapLayers)

    def __init__(self, view, request, context, widget):
        self.view = view
        self.request = request
        self.context = context
        self.widget = widget

    def layers(self):
        # shall I use getAllAdapters instead of getNamed?
        layers = []
        useDefaultLayers = getattr(self.widget, 'usedefault', True)
        if useDefaultLayers:
            default_layers = getUtility(IDefaultMapLayers)
            layers.extend(default_layers.layers(self.view, self.request,
                                                self.context, self.widget))

        maplayers = getattr(self.widget, '_layers', None)
        if maplayers:
            for layerid in maplayers:
                if IMapLayer.providedBy(layerid):
                    layers.append(layerid)
                elif isinstance(layerid, basestring):
                    layers.append(getMultiAdapter((self.view,
                                                   self.request,
                                                   self.context,
                                                   self.widget), IMapLayer,
                                                                name=layerid))
                else:
                    raise ValueError("Can't create IMapLayer for %s" % \
                                                                repr(layerid))
        return layers

    @property
    def js(self):
        layers = self.layers()
        return "cgmap.extendconfig({layers: [\n" +\
               ",\n".join([l.jsfactory for l in layers]) + \
               "]}, '%s');" % (self.widget.mapid)
