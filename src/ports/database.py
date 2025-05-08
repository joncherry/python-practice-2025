import abc


class Data(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_hay_price_data")
            and callable(subclass.get_hay_price_data)
            or NotImplemented
        )

    @abc.abstractmethod
    def get_hay_price_data(self=None):
        raise NotImplementedError
