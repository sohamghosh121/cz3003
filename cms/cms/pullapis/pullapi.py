"""
	Abstract class of API pulling modules
"""
from abc import ABCMeta, abstractmethod


class PullAPI:
	"""
        PullAPI abstract class
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def pull_update(self):
    	"""
        	pull_update abstract method
    	"""
        pass
    	