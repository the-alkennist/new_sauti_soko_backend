from django.contrib import admin

# Register your models here.
from apartments.models import Landlord, Room, RoomType, Apartment

admin.site.register(Landlord)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Apartment)

