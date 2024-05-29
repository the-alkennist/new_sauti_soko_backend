from django.db import models
from django.contrib.auth.models import User

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Apartment(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    number_of_rooms = models.IntegerField()
    occupied_rooms = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.number_of_rooms} {self.room_type.name} in {self.apartment.name}'

    @property
    def available_rooms(self):
        return self.number_of_rooms - self.occupied_rooms
