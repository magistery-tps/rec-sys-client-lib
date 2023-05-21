from abc import ABCMeta
from .model  import Model


class Mapper(metaclass=ABCMeta):
    """Common mapper interface. This interface is used for all entity mappers.
    An entity mapper. Mapper subclass convert object from mapper.Model to a dict DTO and vice versa.
    """

    def to_model(self, dto):
        """Convert a DTO dict model to a mapper.Model object.

        Args:
            dto (dict): Represent a DTO object.

        Returns:
            mapper.Model: A model object.
        """
        pass

    def to_dto(self, model, host=''):
        """Convert a mapper.Model object to a DTO dict object.

        Args:
            model (mapper.Model): Represent  a mapper.Model object.

        Returns:
            mapper.Model:  a DTO dict object.
        """
        pass