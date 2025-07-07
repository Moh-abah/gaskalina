from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    fixed_location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    fixed_location_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=True, blank=True)  # اسم الحارة
    location_notes = models.TextField(null=True, blank=True)  # ملاحظات عن الموقع

    def __str__(self): 
        return self.username
    



class GasOrder(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_orders')
    order_time = models.DateTimeField(auto_now_add=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lon = models.DecimalField(max_digits=9, decimal_places=6)
    neighborhood = models.CharField(max_length=100)
    location_notes = models.TextField(null=True, blank=True)
    floor_number = models.PositiveIntegerField(null=True, blank=True)       # رقم الطابق
    apartment_number = models.CharField(max_length=20, null=True, blank=True) # رقم الشقة
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    #
    driver = models.ForeignKey('Driver', null=True, blank=True, on_delete=models.SET_NULL, related_name='driver_orders')


    def __str__(self):
        return f"Order {self.id} by {self.customer.username} - {self.status}"


class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    carnumber = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.user.username