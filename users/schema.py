import graphene
from users.mutations import UserRegisterMutation, CustomLoginMutation
from users.queries import UserQuery


class AuthMutation(graphene.ObjectType):
    register = UserRegisterMutation.Field()
    login = CustomLoginMutation.Field()


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
