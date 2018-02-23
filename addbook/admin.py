from django.contrib import admin
# Import the UserProfile model individually.
from .models import UserProfile, AddressBook

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AddressBook)