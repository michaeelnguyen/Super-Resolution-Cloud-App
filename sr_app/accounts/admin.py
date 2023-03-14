from django.contrib import admin

# Register your models here.

from .models import Customer, Employee

admin.site.register(Customer)
admin.site.register(Employee)