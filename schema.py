import graphene
import json
import uuid
from datetime import datetime

# Class that will handle schema for users, aka Post Model
class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


# Class that will handle schema for users, aka Users Model
class User(graphene.ObjectType):
    id = graphene.ID(default_value=uuid.uuid4().__str__())
    username = graphene.String(default_value="")
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return "https://cloudinary.com/{}/{}".format(self.id, self.username)


class CreateUser(graphene.Mutation):
    # This defines the shape of the Users
    users = graphene.Field(User)

    # All mutations must take in arguments
    class Arguments:
        username = graphene.String()

    # Resolver function
    def mutate(self, info, username):
        users = User(username=username)
        return CreateUser(users=users)


class CreatePost(graphene.Mutation):
    # This defines the shape of the Posts
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    # To create a new post, use the mutate resolver
    def mutate(self, info, title, content):
        if info.context["is_authenticated"] == False:
            raise Exception("Not Authenticated...")
        else:
            post = Post(title=title, content=content)
            return CreatePost(post=post)


# Class that will handle the Mutations for users, aka Mutation Model, root mutation
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


# Class that will be used as a Schema for Queries
class Query(graphene.ObjectType):
    # List of possible queries
    hello = graphene.String()
    is_admin = graphene.Boolean()
    users = graphene.List(User, limit=graphene.Int())

    # A resolver for 'hello' query, must prepend 'resolve'
    def resolve_hello(self, info):
        return "world"

    # A resolver for 'is_admin', must be in snake case, must prepend 'resolve'
    def resolve_is_admin(self, info):
        return True

    # A resolver for 'users', must be prepended with 'resolve'
    def resolve_users(self, info, limit=None):
        return [
            User(id=1, username="Bob", created_at=datetime.now()),
            User(id=2, username="Jeff", created_at=datetime.now()),
        ][:limit]


# Create a schema, that will hold how to pass data to query
schema = graphene.Schema(query=Query, mutation=Mutation)

# All data passed to execute, must be in CamelCase
# The execute must be in GraphQL format, so format that way
result = schema.execute(
    """
    {
        users {
            id
            username
            createdAt
            avatarUrl
        }
    }
      
    """,
    context={"is_authenticated": True},
)

if result.errors:
    print(result.errors)
else:
    dict_items = dict(result.data.items())
    json_data = json.dumps(dict_items, indent=2)
    print(json_data)
