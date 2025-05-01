import abc

class Data(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getScrapeResult') and 
                callable(subclass.getScrapeResult) or 
                NotImplemented)

    @abc.abstractmethod
    def getScrapeResult():
        raise NotImplementedError