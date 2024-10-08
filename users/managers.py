from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name=None, last_name=None, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        # Handle missing first_name or last_men
        if first_name is None:
            first_name = extra_fields.get('first_name', 'GoogleUser')  # Default value if first_name is not provided
        if last_name is None:
            last_name = extra_fields.get('last_name', 'LastName')  # Default value if last_name is not provided
        
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, first_name=None, last_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)
