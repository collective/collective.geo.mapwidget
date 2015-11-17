# -*- coding: utf-8 -*-
import collective.geo.mapwidget

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


CGEO_MAPWIDGET = PloneWithPackageLayer(
    bases=(PLONE_APP_CONTENTTYPES_FIXTURE, ),
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
