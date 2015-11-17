# -*- coding: utf-8 -*-
# from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig
from plone.testing import z2


class CGeoMapWidgetLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import Products.ATContentTypes
        xmlconfig.file('configure.zcml',
                       Products.ATContentTypes,
                       context=configurationContext)
        z2.installProduct(app, 'plone.app.blob')
        z2.installProduct(app, 'Products.ATContentTypes')

        import collective.geo.mapwidget
        self.loadZCML(package=collective.geo.mapwidget)

    def setUpPloneSite(self, portal):
        """ do special site setup here"""
        applyProfile(portal, 'Products.ATContentTypes:default')
        applyProfile(portal, 'collective.geo.mapwidget:default')


CGEO_MAPWIDGET = CGeoMapWidgetLayer()

CGEO_MAPWIDGET_INTEGRATION = IntegrationTesting(
    bases=(CGEO_MAPWIDGET, ),
    name="CGEO_MAPWIDGET_INTEGRATION")

CGEO_MAPWIDGET_FUNCTIONAL = FunctionalTesting(
    bases=(CGEO_MAPWIDGET, ),
    name="CGEO_MAPWIDGET_FUNCTIONAL")
