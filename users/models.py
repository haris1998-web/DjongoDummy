from django.contrib.auth.models import AbstractUser, BaseUserManager
from djongo import models
from datetime import datetime


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email can not be empty")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.last_login = datetime.now()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff set to True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser set to True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    _id = models.ObjectIdField()
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address", unique=True)
    name = models.CharField(max_length=30)

    USERNAME = None
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()
