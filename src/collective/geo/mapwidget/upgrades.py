from zope.component.hooks import getSite
from zope.component import getGlobalSiteManager
from Products.CMFCore.utils import getToolByName

default_profile = 'profile-collective.geo.mapwidget:default'


def upgrade_to_20(context):
    """This upgrade step fixes javascript registry and static resources
    """
    context.runImportStepFromProfile(default_profile, 'jsregistry')
    context.runImportStepFromProfile(default_profile, 'controlpanel')

    # install collective.z3cform.mapwidget and colorpicker
    qi = getToolByName(context, 'portal_quickinstaller')

    if not qi.isProductInstalled('collective.z3cform.colorpicker'):
        qi.installProduct('collective.z3cform.colorpicker')

    if not qi.isProductInstalled('collective.z3cform.mapwidget'):
        qi.installProduct('collective.z3cform.mapwidget')
