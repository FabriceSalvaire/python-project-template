####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

####################################################################################################

"""
Singleton snippets.
"""

####################################################################################################

from __future__ import print_function

####################################################################################################

import threading 

####################################################################################################

class singleton(object):

    """ A singleton class decorator.
    
    This implementation doesn't support subclassing.
    """

    ##############################################

    def __init__(self, cls):

        # print('singleton __init__: On @ decoration', cls, sep='\n... ')

        self._cls = cls
        self._instance = None

    ##############################################

    def __call__(self, *args, **kwargs):

        # print('singleton __call__: On instance creation', self, args, kwargs, sep='\n... ')

        if self._instance is None:
            self._instance = self._cls(*args, **kwargs)

        return self._instance

####################################################################################################

def singleton_func(cls):

    """ A singleton function decorator.
    
    This implementation doesn't support subclassing.
    """

    # print('singleton_func: On @ decoration', cls, sep='\n... ')

    instances = {}

    def get_instance(*args, **kwargs):
        # print('singleton_func: On instance creation', cls, sep='\n... ')
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

####################################################################################################

class MetaSingleton(type):

    """ A singleton metaclass.
    
    This implementation supports subclassing and is thread safe.
    """

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        # It is called just after cls creation in order to complete cls.

        # print('MetaSingleton __init__:', cls, class_name, super_classes, class_attribute_dict, sep='\n... ')

        type.__init__(cls, class_name, super_classes, class_attribute_dict)

        cls._instance = None
        cls._rlock = threading.RLock() # A factory function that returns a new reentrant lock object.
        
    ##############################################

    def __call__(cls, *args, **kwargs):

        # It is called when cls is instantiated: cls(...).
        # type.__call__ dispatches to the cls.__new__ and cls.__init__ methods.

        # print('MetaSingleton __call__:', cls, args, kwargs, sep='\n... ')

        with cls._rlock:
            if cls._instance is None:
                cls._instance = type.__call__(cls, *args, **kwargs)

        return cls._instance

####################################################################################################

class monostate(object):

    """ A monostate base class.
    """

    _shared_state = {}

    ##############################################

    def __new__(cls, *args, **kwargs):

        # print('monostate __new__:', cls, args, kwargs, sep='\n... ')

        obj = super(monostate, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state

        return obj

####################################################################################################
#
# End
#
####################################################################################################
