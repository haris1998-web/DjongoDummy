import graphene


class UserQuery(graphene.ObjectType):
    user = graphene.String()

    @staticmethod
    def resolve_user(self):
        return None