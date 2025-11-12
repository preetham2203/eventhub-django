from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Event, Registration
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Event.objects.select_related('category', 'organizer').all()
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
            
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        try:
            with transaction.atomic():
                event = Event.objects.select_for_update().get(pk=pk)
                
                if Registration.objects.filter(event=event, user=request.user).exists():
                    return Response(
                        {'error': 'You are already registered for this event'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                if event.registered_count >= event.max_attendees:
                    return Response(
                        {'error': 'Sorry, this event is full!'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                Registration.objects.create(event=event, user=request.user)
                
                return Response(
                    {'message': f'Successfully registered for {event.title}!'},
                    status=status.HTTP_201_CREATED
                )
                
        except Event.DoesNotExist:
            return Response(
                {'error': 'Event not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Registration failed. Please try again.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unregister(self, request, pk=None):
        try:
            with transaction.atomic():
                event = Event.objects.select_for_update().get(pk=pk)
                registration = Registration.objects.filter(event=event, user=request.user).first()
                
                if registration:
                    registration.delete()
                    return Response(
                        {'message': f'Successfully unregistered from {event.title}'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': 'You are not registered for this event'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
        except Exception as e:
            return Response(
                {'error': 'Unregistration failed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-events')
    def my_events(self, request):
        events = Event.objects.filter(organizer=request.user)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='registered-events')
    def registered_events(self, request):
        events = Event.objects.filter(registration__user=request.user)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)