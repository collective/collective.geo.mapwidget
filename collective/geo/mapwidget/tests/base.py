# from Products.Five import zcml
from Zope2.App import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_product():
    """Set up the package and its dependencies.
    """

    fiveconfigure.debug_mode = True
    import collective.geo.mapwidget
    zcml.load_config('configure.zcml', collective.geo.mapwidget)

    fiveconfigure.debug_mode = False


setup_product()
ptc.setupPloneSite(
    extension_profiles=('collective.geo.mapwidget:default',
                        'collective.geo.settings:default',
                        'collective.geo.mapwidget:default',)
)


class TestCase(ptc.PloneTestCase):
    pass


class FunctionalTestCase(ptc.FunctionalTestCase):

    def afterSetUp(self):

        from collective.geo.settings.utils import geo_settings
        geo_settings(self.portal).default_layers = [u'osm',
                                                    u'google_ter',
                                                    u'google_hyb',
                                                    u'google_sat',
                                                    u'google_map']
