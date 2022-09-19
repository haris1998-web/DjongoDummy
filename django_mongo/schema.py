import graphene
from graphql_auth.schema import UserQuery
from graphql_auth import mutations
from users.schema import Query as users_query, Mutation as users_mutation


class Query(users_query):
    pass

class Mutation(users_mutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)