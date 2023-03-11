from django.contrib.auth.models import BaseUserManager
from django.db import models


class Usermanayer(BaseUserManager, models.Manager):
    #este es el maneyer de creacion del los ususarios 

    def _create_user(self, username, gmail, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            username=username,
            gmail=gmail,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self.db)

    def create_user(self, username, gmail, password, **extra_fields):
         return self._create_user(username, gmail, password,False,False,True, **extra_fields)
    
    def create_superuser(self, username, gmail, password, **extra_fields):
        return self._create_user(username, gmail,password, True, True, True, **extra_fields)
    