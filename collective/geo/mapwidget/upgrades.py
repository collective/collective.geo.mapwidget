from zope.component.hooks import getSite
from zope.component import getGlobalSiteManager

default_profile = 'profile-collective.geo.mapwidget:default'


def upgrade_to_17(context):
    """This upgrade step fixes javascript registry and static resources
    """
    context.runImportStepFromProfile(default_profile, 'jsregistry')
    context.runImportStepFromProfile(default_profile, 'controlpanel')
