/*global window, jQuery, document, OpenLayers, google*/

/* cgmap is a namespace object, holding all relevant javascript
 * variables and methods used within collective.geo.*
 */

/* define a few common Openlayers methods to be reused */


(function ($) {
    "use strict";

    /* initalize all maps after page has been loaded and the dom tree
     * is fully intstantiated
     */
    $(window).bind("load", function () {
        var els = $('div.widget-cgmap').collectivegeo({
            // center: new OpenLayers.LonLat('45.00', '7.3'),
            // zoom: 3,
            lang: 'it'
        });

        // $(els[0]).collectivegeo(
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

        // $(els[1]).collectivegeo(
        //     'add_markeredit_layer',
        //      'lon','lat','zoom'
        // );
        // alert($('#geoshapemap').is(":visible"));
    });


    // $(window).bind('mapload', function (evt, widget) {
    //     widget.addLayers(
    //         [
    //             function () {
    //                 return new OpenLayers.Layer.Google(
    //                     'Terrain (Google)',
    //                     {
    //                         type: google.maps.MapTypeId.TERRAIN,
    //                         numZoomLevels: 20,
    //                         sphericalMercator: true,
    //                         transitionEffect: 'resize'
    //                     }
    //                 );
    //             }
    //         ],
    //         'geoshapemap'
    //     );

    // });
}(jQuery));

