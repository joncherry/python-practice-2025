import abc

class DatabaseData(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getTableSingleRow') and 
                callable(subclass.getTableSingleRow) or 
                NotImplemented)

    @abc.abstractmethod
    def getTableSingleRow(table_name: str):
        raise NotImplementedError