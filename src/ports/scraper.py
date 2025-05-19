import abc


class Data(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_scrape_result")
            and callable(subclass.get_scrape_result)
            or NotImplemented
        )

    @abc.abstractmethod
    def get_scrape_result(self=None):
        raise NotImplementedError
