import graphene 
from graphene import relay 
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField 
from models import Country as CountryModel, DayData as DayDataModel, DatabaseUpdate as DBUpdate
# import utils 


# country connection createion
class CountryAttribute:
    name = graphene.String(description = "name of country") 
    total_cases = graphene.Int(description = 'total number of cases within the country') 
    total_deaths = graphene.Int(description = 'total number of deaths within the country') 
    history = graphene.Field(DayDataModel, description = 'the list of related objects containing ')


class Country(SQLAlchemyObjectType):
    class Meta:
        model = CountryModel 
        interfaces = (relay.Node, )


class CountryConnection(relay.Connection):
    class Meta:
        node = Country 


# class UpdatePlanetInput(graphene.InputObjectType, CountryAttribute):
#     id = graphene.ID(required = True, description = "Global Id of the country") 


# class UpdateCountry(graphene.Mutation):
#     country = graphene.Field(lambda: Country, description="Country created by this mutation") 

#     class Arguments:
#         input = UpdatePlanetInput(required = True) 
    
#     def mutate(self, info, input):
#         from models import db_session
#         data = utils.input_to_dictionary(input)
        
#         country = db_session.query(CountryModel).filter_by(id = data['id'])
#         country.update(data) 
#         db_session.commit()
#         country = db_session.query(CountryModel).filter_by(id = data['id']).first() 

#         return UpdateCountry(country = country)


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

class DatabaseUpdate(SQLAlchemyObjectType):
    class Meta: 
        model = DBUpdate 
        interfaces = (relay.Node, ) 

class DatabaseUpdateConnection(relay.Connection):
    class Meta:
        node = DatabaseUpdate

# --------------------------------------

class Query(graphene.ObjectType):
    node = relay.Node.Field() 
    # retrieve all countries 
    all_countries = SQLAlchemyConnectionField(CountryConnection)
    # retrieve single country 
    country = relay.Node.Field(Country)
    # retrieve all history
    all_history = SQLAlchemyConnectionField(DayDataConnections)
    # retrieve all updates 
    all_updates = SQLAlchemyConnectionField(DatabaseUpdateConnection)

schema = graphene.Schema(query = Query) 
