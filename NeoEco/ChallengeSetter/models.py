from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    eco_rank = models.CharField(max_length=20, default='Bronze')
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    avatar_choice = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=1000, default="Sydney")
    work_address = models.CharField(max_length=1000, default="Sydney")
    quest_id = models.CharField(max_length=500, blank=True, null=True, unique=True, help_text="ID of the currently active quest")
    quest_completed = models.BooleanField(default=False, help_text="Whether the current quest is completed")
    quest_file_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the uploaded file")
    rank = models.CharField(max_length=255, default = 0, null = False)
    objects = UserManager()

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Auto-generate quest_id if not set
        if not self.quest_id:
            last_user = User.objects.order_by('-quest_id').first()
            self.quest_id = last_user.quest_id + 1 if last_user and last_user.quest_id else 1
        super().save(*args, **kwargs)