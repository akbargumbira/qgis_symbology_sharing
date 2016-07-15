# coding=utf-8
import os

from symbology_sharing.utilities import local_collection_path
from symbology_sharing import config


class ResourceHandlerMeta(type):
    """Resource handler meta class definition."""
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            # This is the base class.  Create an empty registry
            cls.registry = {}
        else:
            # This is a derived class.
            # Add the class if it's not disabled
            if not cls.IS_DISABLED:
                interface_id = name.lower()
                cls.registry[interface_id] = cls

        super(ResourceHandlerMeta, cls).__init__(name, bases, dct)


class BaseResourceHandler(object):
    """Abstract class of handler."""
    __metaclass__ = ResourceHandlerMeta

    IS_DISABLED = True

    def __init__(self, collection_id=None):
        """Constructor of the base class."""
        self._collection_id = collection_id
        self._collection = config.COLLECTIONS[self._collection_id]

    @property
    def collection_id(self):
        return self._collection_id

    @property
    def collection(self):
        return self._collection

    @classmethod
    def dir_name(cls):
        """The root directory name for this type of the resource."""
        raise NotImplementedError

    @property
    def resource_dir(self):
        """The root of the resource dir from this type of the resource."""
        resource_dir = os.path.join(
            local_collection_path(self.collection_id), self.dir_name())
        return resource_dir

    def install(self):
        """Install all the resources of this type in the collection."""
        raise NotImplementedError

    def uninstall(self):
        """Uninstall all the resources of this type in the collection."""
        raise NotImplementedError
