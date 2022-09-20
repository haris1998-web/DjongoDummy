import graphene
from djongo import models
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field

from users.models import User


@convert_django_field.register(models.ObjectIdField)
def convert_object_id_field(field, registry=None):
    return graphene.String()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'
        field_overrides = {
            "_id": convert_object_id_field
        }
