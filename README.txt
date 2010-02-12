Introduction
============

collective.geo.mapwidget provides a graphical user interface to store settings of collective.geo packages.
Also provides a set of macros to display openlayer map in Plone with a z3cform widget and macros

Requirements
------------
* plone >= 3.2.1
* plone.app.z3cform
* collective.geo.openlayers

Installation
============
Just a simple easy_install collective.geo.mapwidget is enough.

Alternatively, buildout users can install collective.geo.mapwidget as part of a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs = 
            zope.i18n>=3.4
            z3c.form==1.9
            collective.geo.mapwidget
        ...
        [instance]
        ...
        zcml = 
            collective.geo.mapwidget

Install this product from the Plone control panel.


Contributors
============

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Breitkreutz - rockdj
* Gerhard Weis - gweis
