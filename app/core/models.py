import uuid, os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings
from django.db.models.deletion import CASCADE

def recipe_image_file_path(instance, file_name):
    """
        generate filepath for new recipe image
    """
    ext = file_name.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', file_name)

class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**kwargs):
        """
            create base user
        """
        if not email:
            raise ValueError('Email field cannot be empty')
        user = self.model(email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password=None,**kwargs):
        """
            create base user
        """
        user = self.model(email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):

    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return self.name



class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Model for recipe"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=600, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null = True, upload_to = recipe_image_file_path)

    def __str__(self):
        return self.title

