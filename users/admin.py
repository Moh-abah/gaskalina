
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GasOrder, User,Driver

admin.site.register(User, UserAdmin)
admin.site.register(GasOrder)
admin.site.register(Driver)
