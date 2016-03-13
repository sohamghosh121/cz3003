from abc import ABCMeta, abstractmethod


class PullAPI:
    __metaclass__ = ABCMeta

    @abstractmethod
    def pullUpdate(self):
        pass
    	