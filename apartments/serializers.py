from rest_framework import serializers
from .models import Landlord, Apartment, Room, RoomType

class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landlord
        fields = ['id', 'name']

class ApartmentSerializer(serializers.ModelSerializer):
    landlord = serializers.ReadOnlyField(source='landlord.user.username')

    class Meta:
        model = Apartment
        fields = ['id', 'name', 'landlord']

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name']

class RoomSerializer(serializers.ModelSerializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())

    class Meta:
        model = Room
        fields = ['id', 'room_type', 'number_of_rooms', 'occupied_rooms']

    def create(self, validated_data):
        room_type_data = validated_data.pop('room_type')
        if isinstance(room_type_data, dict):
            room_type = RoomType.objects.create(**room_type_data)
        else:
            room_type = room_type_data
        room = Room.objects.create(room_type=room_type, **validated_data)
        return room

    # For GET requests, use RoomTypeSerializer
    def to_representation(self, instance):
        self.fields['room_type'] = RoomTypeSerializer()
        return super().to_representation(instance)