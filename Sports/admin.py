from django.contrib import admin
from .models import Booking, Inventory, Review, Slot, Sport

# Register your models here.

admin.site.register(Sport)
admin.site.register(Inventory)
admin.site.register(Review)
admin.site.register(Slot)
admin.site.register(Booking)