from abc import ABCMeta, abstractmethod


class PullAPI:
    __metaclass__ = ABCMeta

    @abstractmethod
    def pull_update(self):
        pass
    	