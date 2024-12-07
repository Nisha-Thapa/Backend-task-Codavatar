from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


#Creating Cutom User Model so that users of cloud_telephony can independently mannage their virtual phone numbers

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='telephony_user_groups',  # Avoid clash with auth.User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='telephony_user_permissions',  # Avoid clash with auth.User.user_permissions
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class VirtualPhoneNumber(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="virtual_phone_numbers"
    )
    phone_number = models.CharField(max_length=15, unique=True)  # Assuming standard E.164 format
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number


class CallLog(models.Model):
    virtual_phone_number = models.ForeignKey(
        VirtualPhoneNumber,
        on_delete=models.CASCADE,
        related_name="call_logs"
    )
    call_type = models.CharField(
        max_length=10,
        choices=[('INCOMING', 'Incoming'), ('OUTGOING', 'Outgoing')]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()  # store duration of a call in seconds
    details = models.TextField(blank=True, null=True)  # if some details are needed

    def __str__(self):
        return f"{self.call_type} - {self.virtual_phone_number.phone_number}"