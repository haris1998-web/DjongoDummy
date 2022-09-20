from _datetime import datetime

import graphene
from django.contrib.auth import authenticate
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token

from users.models import User
from users.types import UserType


class UserRegisterMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        password = graphene.String(required=True)
        password_confirmation = graphene.String(required=True)

    @staticmethod
    def mutate(self, info,
               email=None, name=None, password=None,
               password_confirmation=None):
        try:
            user = User.objects.filter(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            raise Exception('User already exists!')
        elif password != password_confirmation:
            raise Exception('Passwords do not match!')
        else:
            user_instance = User(name=name, email=email)

            user_instance.set_password(password_confirmation)
            user_instance.is_active = True
            user_instance.is_staff = False
            user_instance.save()

            token = get_token(user_instance)
            refresh_token = create_refresh_token(user_instance)

            return UserRegisterMutation(user=user_instance,
                                        success=True,
                                        token=token,
                                        refresh_token=refresh_token
                                        )


class CustomLoginMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, email=None, password=None):
        user = authenticate(email=email, password=password)

        if user:
            token = get_token(user)
            refresh_token = create_refresh_token(user)

            return CustomLoginMutation(
                success=True,
                token=token,
                refresh_token=refresh_token,
                user=user
            )

        else:
            return CustomLoginMutation(
                success=False,
                token=None,
                refresh_token=None,
                user=None
            )
