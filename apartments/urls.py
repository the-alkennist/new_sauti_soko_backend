from django.urls import path
from .views import ApartmentListCreateView, ApartmentDetailView, RoomListCreateView, RoomDetailView


app_name = "apartments"
urlpatterns = [
    path('apartments/', ApartmentListCreateView.as_view(), name='apartment-list-create'),
    path('apartments/<int:pk>/', ApartmentDetailView.as_view(), name='apartment-detail'),
    path('apartments/<int:apartment_id>/rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
]
