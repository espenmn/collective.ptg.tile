from plone import tiles
from zope.interface import Interface

from Acquisition import aq_inner
from collective.cover import _
from collective.cover.tiles.base import AnnotationStorage
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile

from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

import time

from plone.app.uuid.utils import uuidToObject
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from zope import schema

from plone.memoize.instance import memoize

from zope.component import getMultiAdapter


class IPtgTile(IPersistentCoverTile):
    """  settings for gallery  tile """
    
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )
    
    gallerypath = schema.TextLine(
        title=_(u"label_width_title_gallerytile_setting", default=u"Which Gallery"),
        description=_(u"label_width_description_gallerytile_setting", 
        default=u"The path to the gallery you want to  show."),
        default=u'my/path',
        required=True)

class PtgTile(PersistentCoverTile):

    implements(IPtgTile)

    index = ViewPageTemplateFile('ptg_tile.pt')

    is_configurable = False

    def is_set(self):
        return self.data['gallerypath']
        
    def truegallery_path(self):
		path = self.data['gallerypath']
		path = str(path)
		if path.startswith('/'):
			path = path[1:]
		return portal.restrictedTraverse(path, default=False)
		#return path
			    
    @property
    @memoize
    def gallery_path(self):
		context=self.context
		
		try:
			portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
			portal = portal_state.portal()
			path = str(self.data['gallerypath'])
			if path.startswith('/'):
				path = path[1:]
				
			return portal.restrictedTraverse(path, default=False)
		except:
			return False
			