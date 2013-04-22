/*global window, jQuery, document, OpenLayers*/

(function ($) {
    "use strict";


    if ((typeof window.collectivegeo) === 'undefined') {
        window.collectivegeo = {};
    }
    var collectivegeo = window.collectivegeo, methods;

    collectivegeo.MapWidget = function (trigger, settings) {
        var self = this;

        self.mapid = $(trigger).attr('id');
        self.map = null;
        self.trigger = trigger;
        self.settings = settings;
        self.initMap();
        return self;
    };

    collectivegeo.MapWidget.prototype = {

        initMap: function () {
            var self = this;
            self.map = new OpenLayers.Map(
                self.mapid,
                self.getDefaultOptions()
            );
            self.addLayers();
            self.setCenter();
        },

        setCenter: function () {
            var self = this,
                center = self.settings.center,
                displayProjection = self.map.displayProjection;

            if (!center) {
                self.map.zoomToMaxExtent();
            } else {
                if (displayProjection) {
                    center.transform(
                        displayProjection,
                        self.map.getProjectionObject()
                    );
                }

                self.map.setCenter(center, self.settings.zoom);
            }

        },

        addLayers: function (layer) {
            var self = this,
                layers = self.getDefaultLayers(),
                i;

            for (i = 0; i < layers.length; i += 1) {
                self.map.addLayer(layers[i]());
            }

        },

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
        }
    };


    methods = {
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
                    mapwidget = new collectivegeo.MapWidget(this, settings);
                    $(this).data('collectivegeo', {
                        target: $this,
                        mapwidget: mapwidget
                    });
                }
            });

        },

        destroy : function () {
            return this.each(function () {
                var $this = $(this),
                    data = $this.data('collectivegeo');

                data.collectivegeo.remove();
                $this.removeData('collectivegeo');
            });
        },

        refresh : function (content) {
          // TODO: refersh map
        },

        // data: function () {
        //     return this.each(function () {
        //         return $(this).data('collectivegeo');
        //     });
        // },

        addEditLayer: function () {
            var $this = $(this),
                data = $this.data('collectivegeo'),
                edit_layer,
                elctl;

            edit_layer = function () {
                return new OpenLayers.Layer.Vector('Edit');
            };

            elctl = new OpenLayers.Control.WKTEditingToolbar(
                edit_layer(),
                {wktid: 'form-widgets-wkt'}
            );

            data.mapwidget.map.addControl(elctl);
            elctl.activate();
        }
    };

    $.fn.extend({
        collectivegeomap: function (method) {

            // Method calling logic
            if (methods[method]) {
                return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
            } else if (typeof method === 'object' || !method) {
                return methods.init.apply(this, arguments);
            } else {
                $.error('Method ' +  method + ' does not exist on jQuery.collectivegeomap');
            }

        }
    });


}(jQuery));
