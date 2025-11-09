from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.db.models import Q
from .models import Event, EventCategory, Registration
from .forms import EventForm

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        return queryset.order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Check if user is registered
        if self.request.user.is_authenticated:
            context['is_registered'] = Registration.objects.filter(
                event=event, 
                user=self.request.user
            ).exists()
        else:
            context['is_registered'] = False
            
        return context

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event-list')
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def get_success_url(self):
        return reverse('event-detail', kwargs={'pk': self.object.pk})

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event-list')

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Check if already registered
    if Registration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, 'You are already registered for this event.')
        return redirect('event-detail', pk=pk)
    
    # ✅ ADDED CAPACITY CHECK
    if event.registered_count >= event.max_attendees:
        messages.error(request, 'Sorry, this event is full!')
        return redirect('event-detail', pk=pk)
    
    # Register user
    Registration.objects.create(event=event, user=request.user)
    messages.success(request, f'Successfully registered for {event.title}!')
    return redirect('event-detail', pk=pk)

@login_required
def event_unregister(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = Registration.objects.filter(event=event, user=request.user).first()
    
    if registration:
        registration.delete()
        messages.success(request, f'Successfully unregistered from {event.title}.')
    
    return redirect('event-detail', pk=pk)

@login_required
def my_events(request):
    # Events user is registered for
    registered_events = Event.objects.filter(
        registration__user=request.user
    ).order_by('date')
    
    # Events user organized
    organized_events = Event.objects.filter(organizer=request.user).order_by('-created_at')
    
    return render(request, 'events/my_events.html', {
        'registered_events': registered_events,
        'organized_events': organized_events,
    })