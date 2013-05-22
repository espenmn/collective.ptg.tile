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

#from zope.component import queryMultiAdapter
#from zope.component import getMultiAdapter

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
			

    def populate_with_object(self, obj):
        # check permissions
        super(PtgTile, self).populate_with_object(obj)

        data = {'testingsomething'}
        obj = aq_inner(obj)
        
        data_mgr = ITileDataManager(self)
        data_mgr.set(data)
        tile_storage = AnnotationStorage(self)
        obj_storage = BaseAnnotationStorage(obj)
        for k, v in obj_storage.items():
            tile_storage.storage[k] = v
            tile_storage.storage[k]['modified'] = '%f' % time.time()
            scale_data = obj_storage.storage[k]['data'].open().read()
            tile_storage.storage[k]['data'] = 'somedata'

    def accepted_ct(self):
        """ Return a list of content types accepted.
            Dont think we neeed this for truegallery,
            unless there is a way to search for folders with a certain view set 
            on them
        """
        valid_ct = ['Galleryfolder', 'Folder']
        return valid_ct