from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite

#from zope.i18nmessageid import MessageFactory

#_ = MessageFactory('collective.ptg.tile')


def GalleryVocabulary(context):
    site = getSite()
    catalog = site.portal_catalog    
    results =  catalog.searchResults(getLayout='galleryview')
    galleries= []
   
    for result in results:
   		galleries.append(result.getPath())
   		
    terms = [ SimpleTerm(value=pair, token=pair, title=pair) for pair in galleries ]  
    return SimpleVocabulary(terms)

directlyProvides(GalleryVocabulary, IVocabularyFactory)
