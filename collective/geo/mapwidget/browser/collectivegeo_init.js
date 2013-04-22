/*global window, jQuery, document */

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
        var map = $('div.widget-cgmap').collectivegeomap({
            // center: new OpenLayers.LonLat('45.00', '7.3'),
            // zoom: 3
        });

    });

}(jQuery));

