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
        var els = $('div.widget-cgmap').collectivegeo({
            center: new OpenLayers.LonLat('45.00', '7.3'),
            zoom: 3
        });

        // $(els[0]).collectivegeo(
        //     'add_edit_layer',
        //     'form-widgets-wkt'
        // );

        // $(els[1]).collectivegeo(
        //     'add_markeredit_layer'
        // );
        // alert($('#geoshapemap').is(":visible"));
    });

}(jQuery));

