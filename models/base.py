from sqlalchemy.ext.declarative import declarative_base
class ModelBase(object):
    """Baseclass for custom user models."""

    #: the query class used. The `query` attribute is an instance
    #: of this class. By default a `BaseQuery` is used.
    query_class = BaseQuery

    #: an instance of `query_class`. Can be used to query the
    #: database for instances of this model.
    query = None
    
Model = declarative_base(cls=ModelBase)
