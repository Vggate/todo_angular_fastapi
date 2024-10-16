import datetime
from typing import Optional, List, Any, Dict

from sqlalchemy import Column, Integer, Identity, event
from sqlalchemy.orm import Mapped, Session, Query, DeclarativeBase

from ..exceptions import ValidationError


class Environment:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def __getitem__(self, item) -> Optional[Any]:
        """
        A method to retrieve an entity from the registry based on its tablename.

        :param item: The tablename of the entity to retrieve.
        :return: The entity if found, else None.
        """
        for mapper in Base.registry.mappers:
            if mapper.entity.__tablename__ == item:
                return mapper.entity(env=self)
        else:
            return None


class Base(DeclarativeBase):
    _name = None
    __tablename__ = None

    id: Mapped[int] = Column(Integer, Identity(), primary_key=True, comment='ID')

    def __init__(self, env: Optional[Environment] = None):
        super().__init__()
        self.env = env

    @staticmethod
    @event.listens_for(Session, 'loaded_as_persistent')
    def _set_attribute(session, obj):
        obj.env = Environment(session)

    def create(self, values: Dict[str, Any]) -> Any:
        """
        Create a new object with the given values.

        :param values: A dictionary containing field names and their corresponding values.
        :type values: Dict[str, Any]
        :return: The newly created object.
        :rtype: Any
        """
        obj = self.__class__(self.env)
        for field, value in values.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        return obj.save()

    def save(self) -> Any:
        self.env.db_session.add(self)
        self.env.db_session.flush([self])
        return self

    def update(self, values: Dict[str, Any]) -> Any:
        """
        Update the object's attributes with the values provided in the input dictionary.

        :param values: A dictionary containing key-value pairs to update the object's attributes.
        :type values: Dict[str, Any]
        :return: The saved object after updating its attributes.
        :rtype: Any
        """
        for field in values:
            if hasattr(self, field):
                setattr(self, field, values[field])
        self.updated_at = datetime.datetime.now()
        return self.save()

    def delete(self) -> bool:
        self.env.db_session.delete(self)
        return True

    def browse(self, record_id: int) -> Any:
        """
        Browse method to retrieve a record based on the provided record id.

        :param record_id: An integer representing the unique identifier of the record to retrieve.
        :return: Any object corresponding to the record with the provided record_id.
        """
        return self.env.db_session.query(self.__class__).get(record_id)

    @classmethod
    def _process_order_clause(cls, query: Query, order_clause: str = None) -> Query:
        """
        A method to process the order clause in a query.

        Args:
            query (Query): The query object to process.
            order_clause (str, optional): The order clause string. Defaults to None.

        Returns:
            Query: The processed query object.
        """
        if not order_clause:
            return query
        order_clauses = order_clause.split(',')
        for order_clause in order_clauses:
            field, direction = (order_clause.strip().split(' ') + ['asc'])[:2]
            if direction not in ('desc', 'asc'):
                raise ValidationError(f'Order clause must be `asc` or `desc. `{direction}` was given`', 'SQL-001')
            order_value = getattr(cls, field).asc() if direction == 'asc' else getattr(cls, field).desc()
            query = query.order_by(order_value)
        return query

    def search(self, filters: List = None, order: str = None, offset: int = 0, limit: int = None) -> List[Any]:
        """
        A function that searches based on the provided filters, order, offset, and limit parameters and returns a list of results.

        Parameters:
            filters (list): The list of filters to apply to the search query.
            order (str, optional): The order in which to return the results. Defaults to None.
            offset (int): The number of results to skip before returning any.
            limit (int, optional): The maximum number of results to return. Defaults to None.

        Returns:
            List[Any]: A list of results based on the search criteria.
        """
        query = self.env.db_session.query(self.__class__)
        if filters:
            query = self.env.db_session.query(self.__class__).filter(*filters)
        if order:
            query = self.__class__._process_order_clause(query, order)
        return query.offset(offset).limit(limit).all()

    def get_one(self, filters) -> Any:
        """
        Get one record from the database based on the provided filters and return it or None if not found.
        :param filters: The filters to apply to the query.
        :return: The queried item or None if not found.
        """
        query = self.env.db_session.query(self.__class__).filter(*filters)
        return query.one_or_none()

    def search_count(self, filters) -> int:
        """
        Calculate the count of records that match the given filters.

        :param filters: List of filters to apply to the query
        :type filters: List
        :return: Number of records that match the filters
        :rtype: int
        """
        query: Query = self.env.db_session.query(self.__class__).filter(*filters)
        return query.count()