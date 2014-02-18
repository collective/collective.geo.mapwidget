from plone.indexer.decorator import indexer
from collective.geo.mapwidget.utils import get_feature_styles
from collective.geo.geographer.interfaces import IGeoreferenceable


@indexer(IGeoreferenceable)
def collective_geo_styles(context):
    styles = get_feature_styles(context)
    return styles
