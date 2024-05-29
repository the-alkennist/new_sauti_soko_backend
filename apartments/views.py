from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Apartment, Room, Landlord, RoomType
from rest_framework.response import Response

from .serializers import ApartmentSerializer, RoomSerializer, RoomTypeSerializer


from rest_framework import status

class ApartmentListCreateView(generics.ListCreateAPIView):
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Apartment.objects.filter(landlord__user=self.request.user)

    def perform_create(self, serializer):
        landlord, created = Landlord.objects.get_or_create(user=self.request.user)
        serializer.save(landlord=landlord)
    
    def handle_exception(self, exc):
        # You can customize this based on your error handling needs
        response = super().handle_exception(exc)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            # If the response is Bad Request, print the actual error
            print(exc)
        return response

class ApartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Apartment.objects.filter(landlord__user=self.request.user)

    def perform_update(self, serializer):
        landlord = Landlord.objects.get(user=self.request.user)
        if self.get_object().landlord != landlord:
            raise PermissionDenied("You do not have permission to edit this apartment.")
        serializer.save(landlord=landlord)

    def perform_destroy(self, instance):
        landlord = Landlord.objects.get(user=self.request.user)
        if instance.landlord != landlord:
            raise PermissionDenied("You do not have permission to delete this apartment.")
        instance.delete()



class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        apartment_id = self.kwargs.get('apartment_id')
        return Room.objects.filter(apartment__id=apartment_id, apartment__landlord__user=self.request.user)

    def post(self, request, *args, **kwargs):
        print(f"Request data (POST): {self.request.data}")  # Print request data on POST
        apartment_id = self.kwargs.get('apartment_id')
        apartment = Apartment.objects.get(id=apartment_id, landlord__user=self.request.user)

        rooms_data = request.data.pop('rooms', [])
        created_rooms = []
        errors = []

        for room_data in rooms_data:
            room_data['apartment'] = apartment.id  # Ensure apartment_id is set
            room_type_data = room_data.pop('room_type', None)

            if isinstance(room_type_data, dict):
                room_type_serializer = RoomTypeSerializer(data=room_type_data)
                if room_type_serializer.is_valid():
                    room_type, created = RoomType.objects.get_or_create(**room_type_serializer.validated_data)
                    room_data['room_type'] = room_type.id
                else:
                    print('here3',room_type_serializer.errors)
                    errors.append(room_type_serializer.errors)
                    continue
            elif isinstance(room_type_data, int):
                room_data['room_type'] = room_type_data

            print(room_data)
            room_serializer = RoomSerializer(data=room_data)
            if room_serializer.is_valid():
                room = room_serializer.save(apartment=apartment)
                created_rooms.append(room_serializer.data)
            else:
                print('here',room_serializer.errors)
                errors.append(room_serializer.errors)

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'created_rooms': created_rooms}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        apartment_id = self.kwargs.get('apartment_id')
        apartment = Apartment.objects.get(id=apartment_id, landlord__user=self.request.user)
        serializer.save(apartment=apartment)

    def handle_exception(self, exc):
        # You can customize this based on your error handling needs
        response = super().handle_exception(exc)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            # If the response is Bad Request, print the actual error
            print(exc)
        return response
        
class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(apartment__landlord__user=self.request.user)

    def perform_update(self, serializer):
        room = self.get_object()
        if room.apartment.landlord.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this room.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.apartment.landlord.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this room.")
        instance.delete()
