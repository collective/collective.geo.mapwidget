Introduction
============

collective.geo.mapwidget provides some handy page macros and adapters to easily manage
multiple maps on one page.

.. image:: https://secure.travis-ci.org/collective/collective.geo.mapwidget.png
    :target: http://travis-ci.org/collective/collective.geo.mapwidget

Found a bug? Please, use the `issue tracker`_.

.. contents:: Table of contents


Requirements
============

* geopy >= 0.98
* `Plone`_ >= 4.2
* `plone.app.z3cform`_
* `collective.z3cform.colorpicker`_ >= 1.2
* `collective.geo.openlayers`_ >= 3.1
* `collective.geo.settings`_ >= 3.1


Translations
============

This product has been translated into

- Danish.

- German.

- Spanish.

- French.

- Italian.

- Dutch.

- Chinese Simplified.

- Traditional Chinese.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


Installation
============

This addon can be installed has any other addons, please follow official
documentation_.


Upgrading
=========

Version 2.0
-----------

If you are upgrading from an older version to 2.0, you may need to run
upgrade steps. To do this, follow these steps:

#. Browse to ``portal_setup`` in the ZMI of your site
#. Click onto the ``Upgrades`` tab
#. Select ``collective.geo.mapwidget:default`` from the drop-down list and
   click ``Choose Profile``
#. Observe any available upgrades and click the ``Upgrade`` button if any
   are present.


Contributors
============

* Gerhard Weis - gweis
* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Beitey - davidjb
* Rob Gietema - robgietema
* Leonardo J. Caballero G - macagua
* Denis Krienbühl - href
* Benoît Suttor - bsuttor


.. _Plone: http://plone.org
.. _plone.app.z3cform: http://pypi.python.org/pypi/plone.app.z3cform
.. _collective.z3cform.colorpicker: http://pypi.python.org/pypi/collective.z3cform.colorpicker
.. _collective.geo.openlayers: http://pypi.python.org/pypi/collective.geo.openlayers
.. _collective.geo.settings: http://pypi.python.org/pypi/collective.geo.settings
.. _issue tracker: https://github.com/collective/collective.geo.bundle/issues
.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to
