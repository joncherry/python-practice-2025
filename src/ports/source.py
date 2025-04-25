import abc

class SourceData(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getZillowData') and 
                callable(subclass.getZillowData) or 
                NotImplemented)

    @abc.abstractmethod
    def getZillowData():
        raise NotImplementedError