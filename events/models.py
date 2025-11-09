from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(EventCategory, on_delete=models.PROTECT)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    max_attendees = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        return self.date > timezone.now()
    
    @property
    def registered_count(self):
        return self.registration_set.count()
    
    @property
    def spots_available(self):
        return max(0, self.max_attendees - self.registered_count)

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"