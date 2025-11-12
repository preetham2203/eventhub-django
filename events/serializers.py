from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Registration, EventCategory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    registered_count = serializers.ReadOnlyField()
    spots_available = serializers.ReadOnlyField()
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'category', 'category_id', 'date', 'location',
            'organizer', 'organizer_name', 'max_attendees', 'created_at',
            'image', 'registered_count', 'spots_available', 'is_registered'
        ]
        read_only_fields = ['organizer', 'created_at']

    def get_is_registered(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Registration.objects.filter(event=obj, user=request.user).exists()
        return False

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = EventCategory.objects.get(id=category_id)
        validated_data['category'] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            category_id = validated_data.pop('category_id')
            category = EventCategory.objects.get(id=category_id)
            validated_data['category'] = category
        
        return super().update(instance, validated_data)