import graphene 
from graphene import relay 
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField 
from models import Country as CountryModel, DayData as DayDataModel

# country connection createion
class Country(SQLAlchemyObjectType):
    class Meta:
        model = CountryModel 
        interfaces = (relay.Node, )

class CountryConnection(relay.Connection):
    class Meta:
        node = Country 

# --------------------------------------

# day data connection createion
class DayData(SQLAlchemyObjectType):
    class Meta:
        model = DayDataModel 
        interfaces = (relay.Node, ) 

class DayDataConnections(relay.Connection):
    class Meta:
        node = DayData


# --------------------------------------


class Query(graphene.ObjectType):
    node = relay.Node.Field() 
    # retrieve all countries 
    all_countries = SQLAlchemyConnectionField(CountryConnection)
    # retrieve single country 
    country = relay.Node.Field(Country)

    all_history = SQLAlchemyConnectionField(DayDataConnections)

schema = graphene.Schema(query = Query) 
