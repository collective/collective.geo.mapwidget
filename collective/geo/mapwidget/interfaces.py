from zope.interface import Interface
from zope.interface.common.mapping import IEnumerableMapping
from zope import schema

from collective.geo.mapwidget import GeoMapwidgetMessageFactory as _


class IMaps(IEnumerableMapping):
    """A mapping form mapids to IMapWidgets

    looked up as ((view, request, context), IMaps)
    """


class IMapLayers(IEnumerableMapping):
    """
    A mapping of IMapLayer instances

    specific for IMapWidget... looked up as
      ((view, request, context, mapwidget), name)
    """

    js = schema.TextLine(
        title=_(u"Javascript to configure layers."),
        description=_("Returns some js-code to set up available layers."),
        required=True)


class IMapWidget(Interface):
    """
    Provides configuration options for a specific map widget.
    """
    mapid = schema.TextLine(
        title=_(u"Map id"),
        description=_(u"Used to identify the map in the dom-tree and to "\
                      u"lookup an IMapWidget component if necessary."),
        default=u"default-cgmap",
        required=True)

    klass = schema.TextLine(
        title=_(u"Class attribute"),
        description=_(u"The html element class attribute."),
        default=u"widget-cgmap",
        required=True)

    style = schema.TextLine(
        title=_(u"Style attribute"),
        description=_(u"The html element style attribute."),
        required=False)

    js = schema.Text(
        title=_("Javascript extras"),
        description=_(u"Additional Javascript code inserted after the map"
                      u" widget."),
        required=False)

    layers = schema.Object(
        title=_('Layers'),
        description=_('A mapping from layerids to ILayers'),
        schema=IMapLayers)

    usedefault = schema.Bool(
        title=_(u"Enable default layers."),
        description=_(u"If set to true, the default IMapLayers implementation"
                      u" adds all enabled default layers from the geo settings"
                      u" tool."),
        default=True,
        required=False)

    def addClass(klass):
        '''
        add klass to self.klass
        '''


class IMapView(Interface):
    """
    A view implementing this interface provides configurable
    map widgets.
    """
    # TODO: is this the right field for an IMapView or should it be
    #       mapfields here?
    mapwidgets = schema.Object(
        title=_('Map Widgets'),
        description=_('A mapping from mapids to IMapWidgets'),
        schema=IMaps)


class IMapLayer(Interface):
    """
    A pluggable interface making it easier to configure layers.
    """

    jsfactory = schema.Text(
        title=_(u"Javascript factory"),
        description=_(u"Javascript code which returns a new instance of this "\
                      u"layer and does not expect any parameters"),
        required=True)


class IDefaultMapLayers(Interface):
    """Utility to provide a list of default map layers
    """
