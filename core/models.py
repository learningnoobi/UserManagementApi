from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email,first_name,last_name, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,first_name,last_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email,first_name,last_name, password, **extra_fields)


class Permission(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name
    


class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

