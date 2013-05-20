# -*- coding: utf-8 -*-
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.geo.mapwidget


CGEO_MAPWIDGET = PloneWithPackageLayer(
    zcml_package=collective.geo.mapwidget,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.geo.mapwidget:default',
    name="CGEO_MAPWIDGET")

CGEO_MAPWIDGET_INTEGRATION = IntegrationTesting(
    bases=(CGEO_MAPWIDGET, ),
    name="CGEO_MAPWIDGET_INTEGRATION")

CGEO_MAPWIDGET_FUNCTIONAL = FunctionalTesting(
    bases=(CGEO_MAPWIDGET, ),
    name="CGEO_MAPWIDGET_FUNCTIONAL")
