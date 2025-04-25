import abc

class SourceData(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getHomePriceData') and 
                callable(subclass.getHomePriceData) or 
                NotImplemented)

    @abc.abstractmethod
    def getHomePriceData():
        raise NotImplementedError