import graphene

from users.schema import Query as UsersQuery, Mutation as UsersMutation


class Query(UsersQuery):
    pass


class Mutation(UsersMutation):
    pass


global_schema = graphene.Schema(query=Query, mutation=Mutation)
