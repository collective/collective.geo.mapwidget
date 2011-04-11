from zope.interface import Interface
from zope.component import getAdapters
from collective.geo.settings.vocabularies import baseVocabulary
from collective.geo.mapwidget.interfaces import IMapLayer 

#robert@redcor.ch
#the following try block added for plone 4.1 compatibility
from zope.interface import directlyProvides
try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    # robert@redcor.ch Plone 4.1
    from zope.schema.interfaces import IVocabularyFactory

class maplayersVocab(baseVocabulary):

    @property
    def terms(self):
        all_layers = getAdapters((Interface,Interface,Interface,Interface), IMapLayer)
        for layer_id, layer in all_layers:
            yield((layer_id, layer.Title))
            
#plone 4.1 robert@redcor.ch 
directlyProvides(maplayersVocab, IVocabularyFactory)

