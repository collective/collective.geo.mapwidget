from plone.indexer.decorator import indexer
from collective.geo.settings.interfaces import IGeoFeatureStyle
from .utils import get_feature_styles
from zope.interface import Interface


@indexer(IGeoFeatureStyle)
def collective_geo_styles(context):
    styles = get_feature_styles(context)
    return styles
