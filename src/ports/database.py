import abc

class Data(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getHayPriceData') and 
                callable(subclass.getHayPriceData) or 
                NotImplemented)

    @abc.abstractmethod
    def getHayPriceData():
        raise NotImplementedError