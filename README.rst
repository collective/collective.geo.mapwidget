Introduction
============

``collective.geo.mapwidget`` provides some handy page macros and adapters 
to easily manage multiple maps on one page.

.. contents:: Table of contents


Requirements
============

* geopy >= 0.98
* `Plone`_ >= 4.2
* `plone.app.z3cform`_
* `collective.z3cform.colorpicker`_ >= 1.2
* `collective.geo.openlayers`_ >= 3.1
* `collective.geo.settings`_ >= 3.1


Documentation
=============

Full documentation for end users can be found in the "docs" folder.
It is also available online at https://collectivegeo.readthedocs.io/


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


Tests status
============

This add-on is tested using Travis CI. The current status of the add-on is:

.. image:: https://img.shields.io/travis/collective/collective.geo.mapwidget/master.svg
    :target: https://travis-ci.org/collective/collective.geo.mapwidget

.. image:: http://img.shields.io/pypi/v/collective.geo.mapwidget.svg
   :target: https://pypi.org/project/collective.geo.mapwidget


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.geo.mapwidget/issues
- Source Code: https://github.com/collective/collective.geo.mapwidget
- Documentation: https://collectivegeo.readthedocs.io/


Contributors
============

* Gerhard Weis - gweis
* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Beitey - davidjb
* Rob Gietema - robgietema
* Leonardo J. Caballero G. - macagua
* Denis Krienbühl - href
* Benoît Suttor - bsuttor


License
=======

The project is licensed under the GPL.


.. _Plone: https://plone.org/
.. _plone.app.z3cform: https://pypi.org/project/plone.app.z3cform
.. _collective.z3cform.colorpicker: https://pypi.org/project/collective.z3cform.colorpicker
.. _collective.geo.openlayers: https://pypi.org/project/collective.geo.openlayers
.. _collective.geo.settings: https://pypi.org/project/collective.geo.settings
.. _`opening a ticket`: https://github.com/collective/collective.geo.bundle/issues
.. _documentation: https://docs.plone.org/manage/installing/installing_addons.html
