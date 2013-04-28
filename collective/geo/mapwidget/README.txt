How it Works
============

Let's create a view which should display a map.
    >>> from Products.Five import BrowserView
    >>> class TestView(BrowserView):
    ...    def __call__(self):
    ...        return self.template()

We need a request to instantiate the view
    >>> from zope.publisher.browser import TestRequest
    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> from zope.interface import alsoProvides
    >>> portal = layer['portal']
    >>> request = TestRequest()
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> view = TestView(portal, request)

A small helper method to set the template for a view:
    >>> import os
    >>> from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    >>> from Products.Five.browser.pagetemplatefile import BoundPageTemplate
    >>> from collective.geo.mapwidget import tests
    >>> def setTemplate(view, filename):
    ...     view.template = BoundPageTemplate(ViewPageTemplateFile(
    ...             filename, os.path.dirname(tests.__file__)), view)

We also need a page template to render. In this template we include
all collective.geo macros useful to render the map:

* collectivegeo-macros/openlayers
* collectivegeo-macros/map-widget

    >>> import tempfile
    >>> template = tempfile.mktemp('text.pt')
    >>> open(template, 'w').write('''<html xmlns="http://www.w3.org/1999/xhtml"
    ...       xmlns:metal="http://xml.zope.org/namespaces/metal">
    ...     <head>
    ...      <metal:openlayers
    ...         use-macro="context/@@collectivegeo-macros/openlayers" />
    ...     </head>
    ...     <body>
    ...         <metal:mapwidget
    ...           use-macro="context/@@collectivegeo-macros/map-widget" />
    ...     </body>
    ... </html>
    ... ''')
    >>> setTemplate(view, template)


Render the view
---------------

When we render the view, *map-widget* macro defines the div with class
*widget-cgmap* and includes the layers configuration for that map.

The map will be initialized tacking its configuration like from div
*data* attributes.

These attributes will define:
* the center of the map
* deafult zoom
* language

collectivegeo_init.js looks for elements with class *widget-cgmap*
and use these configuration to initialize Openlayer maps.

    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="default-cgmap" class="widget-cgmap" data-cgeolongitude="0.0" data-cgeolatitude="0.0" data-cgeozoom="10.0">
    ...

TODO: include map configuration with data attributes

OpenLayers Language Files
-------------------------

collective.geo.openlayers provides language files which are automatically
included by the openlayers macro introduced earlier:
'<metal:use use-macro="context/@@collectivegeo-macros/openlayers" />'

This method helps with the language switching in this doctest (not something
you would use in other contexts):

    >>> from zope.annotation.interfaces import IAnnotations
    >>> def set_language(code):
    ...    if getattr(portal.REQUEST, '__annotations__', None):
    ...        del portal.REQUEST.__annotations__  # clear cache
    ...    portal.setLanguage(code)


No language file should be included if the current language is English as
OpenLayers itself is written in English.

    >>> set_language('en')
    >>> 'lang/' in view()
    False

Once we switch to a language supported by OpenLayers we should get a
translated version of OpenLayers

    >>> set_language('de')
    >>> 'lang/de.js' in view()
    True

Switching to an unsupported language should yield English again (no file)

    >>> set_language('ji')
    >>> 'lang/' in view()
    False

A list of supported languages may be acquired through the utils

    >>> from collective.geo.mapwidget import utils
    >>> languages = utils.list_language_files()

    >>> languages['de'] == 'lang/de.js'
    True

    >>> languages['es'] == 'lang/es.js'
    True


Customising the display of map widgets
--------------------------------------

Through collective.geo.settings, we have the ability to set certain options
that cause our map widget to display differently.

In particular, map width and map height are two of these such options
and changing these should result in the style being set on the given map.

These options were introduced for two reasons: one, being that they are useful and two, being that OpenLayers has issues if it is being
loaded whilst not being 'visible' on a page
(for instance, within a jQuery tab, etc) and explicit sizes are not set
(straight CSS against the map does not work).

By default, these settings aren't set, thus no special inline CSS or even
the style="" attribute appears on the page.

Let's check this:

    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="default-cgmap" class="widget-cgmap" data-cgeolongitude="0.0" data-cgeolatitude="0.0" data-cgeozoom="10.0">
    ...

That said, we can set these options and see the change reflected on our
widget. Let's go!

    >>> from zope.component import getUtility, queryAdapter
    >>> from plone.registry.interfaces import IRegistry
    >>> from collective.geo.settings.interfaces import IGeoFeatureStyle

Let's get our site-wide settings and set them.

    >>> geofeaturestyle = getUtility(IRegistry).forInterface(IGeoFeatureStyle)
    >>> geofeaturestyle
    <RecordsProxy for collective.geo.settings.interfaces.IGeoFeatureStyle>

We shouldn't have anything set yet.

    >>> geofeaturestyle.map_width == None
    True
    >>> geofeaturestyle.map_height == None
    True

Our properties are strings so we can set them to anything we want/need.

    >>> geofeaturestyle.map_width = u'50.1234em'
    >>> geofeaturestyle.map_height = u'49.9876%'

Now let's check our map widget.

    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="default-cgmap" class="widget-cgmap" style="width:50.1234em;height:49.9876%;" ...>
    ...

We can just set one of these options to see the result.

    >>> geofeaturestyle.map_width = None
    >>> geofeaturestyle.map_height = u'12.3456%'

    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="default-cgmap" class="widget-cgmap" style="height:12.3456%;" ...>
    ...

So, we can see that if we don't specify options, then we end up with no inline
styles set, and thus our browser will fallback to using CSS (or otherwise).

Clean up our settings for other upcoming tests.

    >>> geofeaturestyle.map_width = geofeaturestyle.map_height = None


Map fields
----------

Another way to render a map is to define an attribute named 'mapfields' on the view.

This field must be a list or tuple and should contain IMapWidget
instances or just strings (or a mix), which are then used to look up an
IMapWidget in the adapter registry.

Let's add an attribute to the view. We also need to adapt the template
slightly.

    >>> from collective.geo.mapwidget.browser.widget import MapWidget
    >>> mw1 = MapWidget(view, request, portal)
    >>> mw1.mapid = 'mymap1'
    >>> mw1.addClass('mymapclass1')
    >>> view.mapfields = [mw1]

Let's examine the result:
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
    ...

If there is more than one entry in mapfields, then only the first one
will be rendered unless we change the template slightly.

    >>> mw2 = MapWidget(view, request, portal)
    >>> mw2.mapid = 'mymap2'
    >>> mw2.addClass('mymapclass2')
    >>> view.mapfields.append(mw2)

Let's examine the result with an unchanged template:
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
    ...

Adapt the template to get both maps. We can do this in various ways.
To render each map individually we have to iterate the list manually. There is
a small helper view which makes things easier later, so let's use it.

    >>> open(template, 'w').write('''<html xmlns="http://www.w3.org/1999/xhtml"
    ...       xmlns:metal="http://xml.zope.org/namespaces/metal">
    ...     <head>
    ...         <metal:use use-macro="context/@@collectivegeo-macros/openlayers" />
    ...     </head>
    ...     <body>
    ...         <tal:omit tal:define="maps view/@@collectivegeo-maps/mapwidgets" tal:omit-tag="">
    ...             <tal:omit tal:define="cgmap maps/mymap1" tal:omit-tag="">
    ...                 <metal:use use-macro="context/@@collectivegeo-macros/map-widget" />
    ...             </tal:omit>
    ...             <tal:omit tal:define="cgmap maps/mymap2" tal:omit-tag="">
    ...                 <metal:use use-macro="context/@@collectivegeo-macros/map-widget" />
    ...             </tal:omit>
    ...         </tal:omit>
    ...     </body>
    ... </html>
    ... ''')
    >>> setTemplate(view, template)

Let's see what happens:
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
    ...
          <div id="mymap2" class="mymapclass2 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
    ...

We can also just iterate over the mapwidgets list:
    >>> open(template, 'w').write('''<html xmlns="http://www.w3.org/1999/xhtml"
    ...       xmlns:metal="http://xml.zope.org/namespaces/metal">
    ...     <head>
    ...         <metal:use use-macro="context/@@collectivegeo-macros/openlayers" />
    ...     </head>
    ...     <body>
    ...         <tal:omit tal:repeat="cgmap view/@@collectivegeo-maps/mapwidgets" tal:omit-tag="">
    ...             <metal:use use-macro="context/@@collectivegeo-macros/map-widget" />
    ...         </tal:omit>
    ...     </body>
    ... </html>
    ... ''')
    >>> setTemplate(view, template)


As our first template was not very sophisticated, we should get the same result:

    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
    ...
          <div id="mymap2" class="mymapclass2 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
    ...

It is also possible to register an IMapWidget as named adapter and just give
it's name in mapfields. IMapMidgets are looked up by ((view, request, context),
name). So let's update our configuraion and fields:

    >>> def mw1factory(view, request, context):
    ...     mw = MapWidget(view, request, context)
    ...     mw.mapid = 'mymap1'
    ...     mw.addClass('mymapclass1')
    ...     return mw
    >>> from zope.component import provideAdapter
    >>> from zope.interface import Interface
    >>> from collective.geo.mapwidget.interfaces import IMapWidget
    >>> provideAdapter(mw1factory,
    ...                (Interface, Interface, Interface),
    ...                IMapWidget, name='mw1')
    >>> view.mapfields = ['mw1', mw2]
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
    ...
          <div id="mymap2" class="mymapclass2 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
    ...

The defaul IMaps implementation complains if an element
in mapfields is not a string or IMapWidget:

    >>> view.mapfields = ['mw1', mw2, None]
    >>> print view()
    Traceback (most recent call last):
    ...
    ValueError: Can't create IMapWidget for None

Now we have covered the most important things about map widgets.
Set us try some things with map layers.

Layers
------

Map widgets can have layers associated with them.
These association is handled similar to the IMapWidget - View associaton above.

An IMapWidget instance has to provide an attribute 'layers',
which is a mapping from layer-id to ILayer instances.

The default IMapWidget implementation provides 'layers' as a
computed attribute.

On access it looks up an IMapLayers - manager implementation which handles
the actual IMapLayer instantiation.

If the widget has an attribute 'usedefault' and it is set to False,
the layer manager ignores all default layers set in the controlpanel,
else all the default layers are added.

Additionally the map widget can provide an attribute '_layers',
 which is a list of names and/or ILayer instances to be added.

As a quick example we can just set the '_layers' attribute for mw1
and we should get an additional layer.


    >>> from collective.geo.mapwidget.maplayers import BingRoadsMapLayer
    >>> mw1._layers = [BingRoadsMapLayer(context=portal)]
    >>> view = TestView(portal, request)
    >>> setTemplate(view, template)
    >>> view.mapfields = [mw1]
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
          <script type="text/javascript">
    $(window).bind('mapload', function (evt, widget) {
        widget.addLayers([
            function(){return new OpenLayers.Layer.TMS('OpenStreetMap'...
    ...
            function(){return new OpenLayers.Layer.Bing({
    ...


Me can register the BingStreetMapLayer as an adapter which allows us to use
just the name to get the same result. ILayers are looked up for ((view,
request, context, widget), name):

    >>> from collective.geo.mapwidget.interfaces import IMapLayer
    >>> provideAdapter(BingRoadsMapLayer,
    ...                (Interface, Interface, Interface, Interface),
    ...                IMapLayer, name='bsm')
    >>> mw1._layers = ['bsm']
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
          <script type="text/javascript">
    $(window).bind('mapload', function (evt, widget) {
        widget.addLayers([
            function(){return new OpenLayers.Layer.TMS('OpenStreetMap'...
    ...
            function(){return new OpenLayers.Layer.Bing({
    ...

If _layers contains somethin which can't be converted into an IMapLayer
instance, me get an exception:

    >>> mw1._layers = ['bsm', None]
    >>> print view()
    Traceback (most recent call last):
    ...
    ValueError: Can't create IMapLayer for None


Let's create a custom layer.

A rather common use-case may be to display a static image on a map.
Let's assume our context is an Image object in Plone (e.g. ATImage),
and we want an Openlayers view with the Image as base-layer (I did not test
whether this layer really works with OL, it should rather demonstrate
the concept).

MapWidgets also support a 'js' attribute to render additional java-script
if necessary.

    >>> from collective.geo.mapwidget.maplayers import MapLayer
    >>> class ImageLayer(MapLayer):
    ...     name = "imagelayer"
    ...
    ...     @property
    ...     def jsfactory(self):
    ...         return """function() {return new OpenLayers.Layer.Image('%s', {url: '%s'});}""" % \
    ...    (self.context.Title(), self.context.absolute_url())

An 'Image Layer' is a rather generic component, so it might be useful to
register it as an adapter. (Probably just for IATImage context objects?)

    >>> provideAdapter(ImageLayer,
    ...                (Interface, Interface, Interface, Interface),
    ...                IMapLayer, name='image')


As this becomes an unprojected base layer we don't want the default
base layers

    >>> mw1.usedefault = False
    >>> mw1._layers = ['image']
    >>> mw1.js = "\n// a place to add additional js\n"
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap" ...>
            <!-- openlayers map -->
          </div>
          <script type="text/javascript">
    $(window).bind('mapload', function (evt, widget) {
        widget.addLayers([
            function() {return new OpenLayers.Layer.Image('Plone site', {url: 'http://nohost/plone'});}
        ], 'mymap1');
    });
    <BLANKLINE>
    </script>
          <script type="text/javascript">
    // a place to add additional js
    </script>
    ...

More fancy things cam be done by turning _layers into a computed property.
This way it is possible to return only those layers of current interest.

It is also possible to register a different IMapLayers instance,
which uses some other algorithm to find all default and custom layers.


And another small test to get a 100% test coverage report:

    >>> mw1.klass = None
    >>> mw1.addClass('myclass')
    >>> mw1.klass
    u'myclass'


