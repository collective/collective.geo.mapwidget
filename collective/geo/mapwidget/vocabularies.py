from zope.interface import Interface
from zope.component import getAdapters
from collective.geo.settings.vocabularies import baseVocabulary
from collective.geo.mapwidget.interfaces import IMapLayer


class maplayersVocab(baseVocabulary):

    @property
    def terms(self):
        all_layers = getAdapters((Interface,
                        Interface, Interface, Interface), IMapLayer)
        for layer_id, layer in all_layers:
            yield((layer_id, layer.Title))
