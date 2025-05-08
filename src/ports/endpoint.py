import abc


class Data(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_endpoint_report")
            and callable(subclass.get_endpoint_report)
            or NotImplemented
        )

    @abc.abstractmethod
    def get_endpoint_report(self=None):
        raise NotImplementedError
