from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            customer_First_Name=instance.first_name,
            customer_Last_Name=instance.last_name,
            customer_Email=instance.email,
        )

post_save.connect(customer_profile, sender=User)