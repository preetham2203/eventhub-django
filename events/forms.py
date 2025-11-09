from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'date', 'location', 'max_attendees', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event description', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event location'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum attendees'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }