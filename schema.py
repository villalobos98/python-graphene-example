import graphene
import json
from datetime import datetime


# Class that will handle schema for users
class Users(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()


# Class that will be used as a Schema for Queries
class Query(graphene.ObjectType):
    # List of possible queries
    hello = graphene.String()
    is_admin = graphene.Boolean()
    users = graphene.List(Users, limit=graphene.Int())

    # A resolver for 'hello' query
    def resolve_hello(self, info):
        return "world"

    # A resolver for 'is_admin', must be in snake case
    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        return [
            Users(id=1, username='Bob', created_at=datetime.now()),
            Users(id=2, username='Jeff', created_at=datetime.now())
        ][:limit]


# Create a schema, that will hold how to pass data to query
schema = graphene.Schema(query=Query)

# All data passed to execute, must be in CamelCase
# The execute must be in GraphQL format, so format that way
result = schema.execute(
    '''
    {
        users{
        id
        username
        createdAt
        }
    }
    '''
)

dict_result = dict(result.data.items())
json_data = json.dumps(dict_result, indent=2)
print(json_data)
