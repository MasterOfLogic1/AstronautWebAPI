from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and save a regular User with the given email, username, and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        """
        Override the save method so that if the user_id is not set,
        we assign it after the user is saved and a primary key is available.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Only update the user_id if the instance is new and user_id is not already set.
        if is_new and not self.user_id:
            prefix = "ADM" if self.is_superuser else "USR"
            self.user_id = f"{prefix}{self.pk}"
            # Update the database directly to avoid recursive saving
            User.objects.filter(pk=self.pk).update(user_id=self.user_id)
    
    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'