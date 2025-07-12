from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
#time
from django.utils import timezone 
from datetime import timedelta
#OS 
# import os

class UserManager(BaseUserManager):
    """manager for User."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set."))
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """User model with additional fields and roles."""
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        CUSTOMER = "CUSTOMER", _("Customer")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=128)
    is_active = models.BooleanField(_("active"), default=False)
    is_staff = models.BooleanField(_("staff status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    role = models.CharField(
        _("role"), max_length=10, choices=Role.choices, default=Role.CUSTOMER
    )
    otp = models.CharField(_("otp"), max_length=6,null=True,blank=True)
    otp_exp = models.DateTimeField(null = True,blank = True)
    image = models.ImageField(_("image"), blank=True , null=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
    def __str__(self):
        return f"{self.username}"
    def is_otp_expired(self): 
        return self.otp_exp < timezone.now() -  timedelta(minutes=10)