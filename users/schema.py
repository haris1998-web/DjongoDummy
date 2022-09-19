import graphene

class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)