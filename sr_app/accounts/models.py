import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_First_Name = models.CharField(max_length=255, blank=True)
    customer_Last_Name = models.CharField(max_length=255, blank=True)
    customer_Phone_Number= models.CharField(max_length=255, blank=True)
    customer_Email = models.EmailField(max_length=255, blank=True)

    slug = models.SlugField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        ordering = ['customer_Last_Name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.customer_First_Name + ' ' + self.customer_Last_Name
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    emp_First_Name = models.CharField(max_length=255, blank=True)
    emp_Last_Name = models.CharField(max_length=255, blank=True)
    emp_Phone_Number= models.CharField(max_length=255, blank=True)
    emp_Email = models.EmailField(max_length=255, blank=True)
    role = models.CharField(max_length=255, null=True)

    slug = models.SlugField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    class Meta:
        ordering = ['emp_Last_Name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.emp_First_Name + ' ' + self.emp_Last_Name