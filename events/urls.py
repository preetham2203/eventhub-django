from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import EventViewSet

router = DefaultRouter()
router.register('api/events', EventViewSet, basename='events')

urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('add/', views.EventCreateView.as_view(), name='event-add'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-edit'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
    path('<int:pk>/register/', views.event_register, name='event-register'),
    path('<int:pk>/unregister/', views.event_unregister, name='event-unregister'),
    path('my-events/', views.my_events, name='my-events'),
] + router.urls