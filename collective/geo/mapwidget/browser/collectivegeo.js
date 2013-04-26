/*global window, jQuery, document, OpenLayers*/

(function ($) {
    "use strict";
    // = Collective Geo =
    //
    // This is the application that provides Openlayers map
    // infrastructure to collective.geo
    //
    // It lives in {{{window.collectivegeo}}} where it can be fetched
    // to apply customizations.
    if ((typeof window.collectivegeo) === 'undefined') {
        window.collectivegeo = {};
    }
    var App = window.collectivegeo, methods;


    // == MapWidget ==
    //
    // This class contains all method and utilities
    // to manage collective.geo maps
    App.MapWidget = function (trigger, settings) {
        var self = this;

        self.mapid = $(trigger).attr('id');
        self.map = null;
        self.trigger = trigger;
        self.settings = settings;

        // initialize map
        self.initMap();
    };

    // === MapWidget prototype ===
    //
    // extends MapWidget class with some methods
    App.MapWidget.prototype = {

        // === MapWidget.initMap ===
        //
        // Init a map with default options and set default center and zoom
        initMap: function () {
            var self = this,
                legend_id;

            self.map = new OpenLayers.Map(
                self.mapid,
                self.getDefaultOptions()
            );

            // setup language
            if (self.settings.lang) {
                OpenLayers.Lang.setCode(self.settings.lang);

            }

            $(window).trigger('mapload', self);

            // setup a default layers
            if (self.map.layers.length === 0) {
                self.addLayers(self.getDefaultLayers());

            }

            if (self.settings.center && self.settings.zoom) {
                self.setCenter(self.settings.center, self.settings.zoom);
            } else {
                self.map.zoomToExtent();
            }

            // TODO: call this method to resize maps on hidden divs
            // self.map.updateSize();

        },

        // === MapWidget.setCenter(center, zoom) ===
        setCenter: function (center, zoom) {
            var self = this,
                displayProjection = self.map.displayProjection;

            if (displayProjection) {
                center.transform(
                    displayProjection,
                    self.map.getProjectionObject()
                );
            }

            self.map.setCenter(center, zoom);

        },

        // === MapWidget.addLayers(layers) ===
        addLayers: function (layers, mapid) {
            var self = this,
                i;

            if (mapid && self.mapid !== mapid) {
                return null;
            }

            for (i = 0; i < layers.length; i += 1) {
                self.map.addLayer(layers[i]());
            }

        },

        // === MapWidget.getDefaultLayers ===
        // return {{list}} of Openlayers layers
        getDefaultLayers: function () {
            var self = this,
                layers = [];
            layers.push(function () {
                return new OpenLayers.Layer.WMS(
                    "OpenLayers WMS",
                    "http://vmap0.tiles.osgeo.org/wms/vmap0",
                    {layers: "basic"}
                );
            });
            return layers;
        },

        // === MapWidget.getDefaultOptions ===
        getDefaultOptions: function () {
            return $.extend({
                theme: null, // disable default theme
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326"),
                units: "m",
                numZoomLevels: 19,
                controls: [
                    new OpenLayers.Control.ArgParser(),
                    new OpenLayers.Control.Attribution(),
                    new OpenLayers.Control.LayerSwitcher({
                        roundedCorner: false
                    }),
                    new OpenLayers.Control.Navigation({
                        zoomWheelEnabled: false,
                        dragPanOptions: {
                            enableKinetic: true
                        }
                    }),
                    new OpenLayers.Control.Zoom()
                ]
            }, this.settings.map_defaults);
        },

        osmGetTileURL: function (bounds) {
            var res = this.map.getResolution(),
                x = Math.round((bounds.left - this.maxExtent.left) /
                               (res * this.tileSize.w)),
                y = Math.round((this.maxExtent.top - bounds.top) /
                               (res * this.tileSize.h)),
                z = this.map.getZoom() + this.zoomOffset,
                limit = Math.pow(2, z);

            if (y < 0 || y >= limit) {
                return OpenLayers.Util.getImagesLocation() + "404.png";
            } else {
                x = ((x % limit) + limit) % limit;
                return this.url + z + "/" + x + "/" + y + "." + this.type;
            }
        }

    };

    // == WKTEditingToolbar ==
    //
    // This Openlayers control creates a toolbar to draw features
    // on a map.
    // It can draw points, lines, and polygons
    // and store it in WKT format
    OpenLayers.Control.WKTEditingToolbar = OpenLayers.Class(
        OpenLayers.Control.Panel,
        {

            initialize: function (layer, options) {
                var controls = [
                        new OpenLayers.Control.Navigation(),
                        new OpenLayers.Control.DrawFeature(
                            layer,
                            OpenLayers.Handler.Point,
                            {
                                'displayClass': 'olControlDrawFeaturePoint'
                            }
                        ),
                        new OpenLayers.Control.DrawFeature(
                            layer,
                            OpenLayers.Handler.Path,
                            {
                                'displayClass': 'olControlDrawFeaturePath'
                            }
                        ),
                        new OpenLayers.Control.DrawFeature(
                            layer,
                            OpenLayers.Handler.Polygon,
                            {
                                'displayClass': 'olControlDrawFeaturePolygon'
                            }
                        ),
                        new OpenLayers.Control.ModifyFeature(layer, {
                            mode: OpenLayers.Control.ModifyFeature.RESHAPE || OpenLayers.Control.ModifyFeature.DRAG
                        })
                    ],
                    geomwkt,
                    in_options,
                    format,
                    feat;

                OpenLayers.Control.Panel.prototype.initialize.apply(
                    this,
                    [options]
                );

                this.addControls(controls);
                this.defaultControl = this.controls[5];

                // init edit layer features
                if (this.wktid) {
                    geomwkt = $('#' + this.wktid).val();
                    in_options = {
                        internalProjection: layer.map.getProjectionObject(),
                        externalProjection: layer.map.displayProjection
                    };
                    format = new OpenLayers.Format.WKT(in_options);
                    feat = format.read(geomwkt);

                    if (feat) {
                        layer.addFeatures([feat]);
                        layer.map.zoomToExtent(layer.getDataExtent());
                    }
                }

                layer.events.register(
                    "featureadded",
                    this,
                    this.updateWKTWidget
                );
                layer.events.register(
                    "featuremodified",
                    this,
                    this.updateWKTWidget
                );

                // ensure only one feature is on the map
                layer.events.register(
                    "beforefeaturesadded",
                    this,
                    function (evt) {
                        evt.object.destroyFeatures();
                    }
                );
            },

            updateWKTWidget: function (evt) {
                var out_options = {
                        internalProjection: evt.object.map.getProjectionObject(),
                        externalProjection: evt.object.map.displayProjection
                    },
                    format = new OpenLayers.Format.WKT(out_options);
                $('#' + this.wktid).val(format.write(evt.feature));
                format.destroy();
            },

            CLASS_NAME: 'OpenLayers.Control.EditingToolbar'

        }
    );

    // == MarkerEditingToolbar ==
    //
    // This Openlayers control creates a toolbar to draw points on a map.
    OpenLayers.Control.MarkerEditingToolbar = OpenLayers.Class(
        OpenLayers.Control.Panel,
        {

            initialize: function (layer, options) {
                OpenLayers.Control.Panel.prototype.initialize.apply(
                    this,
                    [options]
                );

                var controls = [
                        new OpenLayers.Control.Navigation(),
                        new OpenLayers.Control.DrawFeature(
                            layer,
                            OpenLayers.Handler.Point,
                            {
                                'displayClass': 'olControlDrawFeaturePoint'
                            }
                        ),
                        new OpenLayers.Control.ModifyFeature(layer)
                    ],
                    point;

                this.addControls(controls);
                this.defaultControl = this.controls[0];

                // setup form events
                if (this.lonid && this.latid) {
                    point = new OpenLayers.Geometry.Point(
                        $('#' + this.lonid).val(),
                        $('#' + this.latid).val()
                    );
                    if (layer.map.displayProjection) {
                        point.transform(
                            layer.map.displayProjection,
                            layer.map.getProjectionObject()
                        );
                    }

                    layer.addFeatures(
                        [new OpenLayers.Feature.Vector(point)]
                    );
                    layer.events.register(
                        "featureadded",
                        this,
                        this.updateForm
                    );
                    layer.events.register(
                        "featuremodified",
                        this,
                        this.updateForm
                    );
                }

                if (this.zoomid) {
                    layer.map.events.register(
                        "zoomend",
                        this,
                        this.updateZoom
                    );
                }

                // ensure only one feature is on the map
                layer.events.register(
                    "beforefeaturesadded",
                    this,
                    function (evt) {
                        evt.object.destroyFeatures();
                    }
                );
            },

            updateZoom: function (evt) {
                $('#' + this.zoomid).val(evt.object.getZoom());
            },

            updateForm: function (evt) {
                var lonlat = new OpenLayers.LonLat(
                    evt.feature.geometry.x,
                    evt.feature.geometry.y
                );
                if (evt.object.map.displayProjection) {
                    lonlat.transform(
                        evt.object.map.getProjectionObject(),
                        evt.object.map.displayProjection
                    );
                }
                $('#' + this.lonid).val(lonlat.lon);
                $('#' + this.latid).val(lonlat.lat);
            },

            CLASS_NAME: 'OpenLayers.Control.EditingToolbar'
        }
    );

    // == JQuery plugin's methods ==
    //
    // this object contains all jQuery's plugin methods.
    methods = {
        // === init ===
        // initialize the map
        init : function (options) {

            return this.each(function () {
                var settings = $.extend(true, {
                    imgpath: '/',
                    center: null,
                    zoom: null
                }, options),
                    $this = $(this),
                    data = $this.data('collectivegeo'),
                    mapwidget;

                // If the plugin hasn't been initialized yet
                if (!data) {
                    mapwidget = new App.MapWidget(this, settings);
                    $(this).data('collectivegeo', {
                        target: $this,
                        mapwidget: mapwidget
                    });
                }
            });

        },

        // === destroy ===
        //
        // this method remove all references to collectivegeo plugin
        destroy : function () {
            return this.each(function () {
                var $this = $(this),
                    data = $this.data('collectivegeo');

                data.collectivegeo.remove();
                $this.removeData('collectivegeo');
            });
        },

        // === add_layers ===
        //
        // add layers to a map passing a list of layers incapsulated
        // in a function:
        //
        // Usage:
        // {{{
        // $('#map').collectivegeo();
        //
        // $('#map').collectivegeo(
        //     'add_layer',
        //     function () {
        //         return new OpenLayers.Layer.Google(
        //             'Terrain (Google)',
        //             {
        //                 type: google.maps.MapTypeId.TERRAIN,
        //                 numZoomLevels: 20,
        //                 sphericalMercator: true,
        //                 transitionEffect: 'resize'
        //             }
        //         );
        //     }
        // );
        // }}}
        add_layers: function (layers) {
            return this.each(function () {
                var $this = $(this),
                    data = $this.data('collectivegeo');
                data.mapwidget.addLayers(layers);
            });
        },

        // === refresh ===
        //
        // this method refresh the map using Openlayers
        // {{{updateSize}}} method
        refresh: function (layers) {
            return this.each(function () {
                var $this = $(this),
                    data = $this.data('collectivegeo');
                data.mapwidget.map.updateSize();

            });
        },

        // === add_edit_layer ===
        //
        // This method add an edit layer to the map
        // that can store values to a textarea element in WKT format.
        //
        // Usage:
        // {{{
        // $(window).bind("load", function () {
        //   var maps = $('div.widget-cgmap').collectivegeo({
        //      center: new OpenLayers.LonLat('45.00', '7.3'),
        //      zoom: 3
        // });
        //
        // $(maps[0]).collectivegeo('add_edit_layer','textarea-id');
        //
        // }}}
        add_edit_layer: function (wkt_input_id) {
            return this.each(function () {
                var $this = $(this),
                    data = $this.data('collectivegeo'),
                    map = data.mapwidget.map,
                    edit_layer,
                    elctl;

                edit_layer = new OpenLayers.Layer.Vector('Edit');
                map.addLayer(edit_layer);

                elctl = new OpenLayers.Control.WKTEditingToolbar(
                    edit_layer,
                    {wktid: wkt_input_id}
                );

                map.addControl(elctl);
                elctl.activate();
            });
        },

        // === add_markeredit_layer ===
        //
        // This method add an edit layer to the map specific
        // to register a point and a zoom level in specific text inputs
        //
        // Usage:
        // {{{
        // $(window).bind("load", function () {
        //   var maps = $('div.widget-cgmap').collectivegeo({
        //      center: new OpenLayers.LonLat('45.00', '7.3'),
        //      zoom: 3
        // });
        //
        // $(maps[0]).collectivegeo(
        //    'add_edit_layer',
        //    'longitude_input_id,
        //    'latitude_input_id,
        //    'zoom_input_id'
        // );
        //
        // }}}
        add_markeredit_layer: function (lonid, latid, zoomid) {
            return this.each(function () {
                var $this = $(this),
                    data = $this.data('collectivegeo'),
                    map = data.mapwidget.map,
                    edit_layer,
                    elctl;

                edit_layer =  new OpenLayers.Layer.Vector(
                    'Marker',
                    {renderOptions: {yOrdering: true}}
                );
                map.addLayer(edit_layer);

                elctl = new OpenLayers.Control.MarkerEditingToolbar(
                    edit_layer,
                    {
                        lonid: lonid,
                        latid: latid,
                        zoomid: zoomid
                    }
                );
                map.addControl(elctl);
                elctl.activate();

                data.mapwidget.setCenter(
                    new OpenLayers.LonLat(
                        $('#' + lonid).val(),
                        $('#' + latid).val()
                    ),
                    $('#' + zoomid).val()
                );
            });

        },

        add_geocoding: function () {
        }
    };


    // == collectivegeo JQuery plugin ==
    //
    // This JQuery plugin allows to create a collective.geo map
    // for each element
    //
    // Usage:
    // {{{
    // $(window).bind("load", function () {
    //   $('div.widget-cgmap').collectivegeo({
    //      center: new OpenLayers.LonLat('45.00', '7.3'),
    //      zoom: 3
    // });
    // }}}
    $.fn.extend({
        collectivegeo: function (method) {

            // Method calling logic
            if (methods[method]) {
                return methods[method].apply(
                    this,
                    Array.prototype.slice.call(arguments, 1)
                );
            } else if (typeof method === 'object' || !method) {
                return methods.init.apply(this, arguments);
            } else {
                $.error(
                    'Method ' +  method + ' does not exist on jQuery.collectivegeo'
                );
            }

        }
    });


}(jQuery));
