import os
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from accounts.models import Customer, Employee

# Utility function to create a file path based on the type of User and Photo objects
def get_user_directory_path(instance, filename):
       # CUSTOMER_MEDIA_ROOT/<customer_uuid>/<filename>
   if isinstance(instance, Photo):
       if instance.user.is_superuser:
           return f"admin/{filename}"
       elif isinstance(instance.user, Customer):
           return f"{instance.user.customer.uuid}/{filename}"
       elif isinstance(instance.user, Employee):
           return f"{instance.user.employee.uuid}/{filename}"
       else:
           raise NotImplementedError(f"Unknown user type: {type(instance.user)}")
   elif isinstance(instance, SRPhoto):
       if instance.user.is_superuser:
           return f"results/{filename}"
       elif isinstance(instance.user, Customer):
           return f"{instance.user.customer.uuid}/{filename}"
       elif isinstance(instance.user, Employee):
           return f"{instance.user.employee.uuid}/{filename}"
       else:
           raise NotImplementedError(f"Unknown user type: {type(instance.user)}")
   elif isinstance(instance, User):
       if isinstance(instance.customer, Customer):
           return f"{instance.customer.uuid}/"
       elif isinstance(instance.employee, Employee):
           return f"{instance.employee.uuid}/"
       else:
           raise NotImplementedError(f"Unknown user type: {type(instance)}")
   else:
       raise NotImplementedError(f"Unknown model type: {type(instance)}")

# Category model class object definition
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

# Photo model class object definition
class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=get_user_directory_path, null=False, blank=False, max_length=255)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True, null=True)

    niqe = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    brisque = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.user:
                self.image.name = f"{self.image.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description

# Corresponding SRPhoto model class object definition
class SRPhoto(models.Model):
   original_photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
   user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
   image = models.ImageField(upload_to=get_user_directory_path, null=False, blank=False, max_length=255)
   model_chosen = models.TextField()
   
   niqe = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
   brisque = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


   def save(self, *args, **kwargs):
       if not self.pk:
           if self.user:
                self.image.name = f"{self.original_photo.image.name.split('.')[0]}_{self.model_chosen}.{self.original_photo.image.name.split('.')[1]}"
       super().save(*args, **kwargs)


   def __str__(self):
       return self.image.name
