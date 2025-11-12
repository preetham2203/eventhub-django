# test_race.py
import threading
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authentication.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from events.models import Event, EventCategory, Registration
from django.utils import timezone

def create_test_event():
    user = User.objects.get(username='preetham')
    category = EventCategory.objects.first()
    
    event = Event.objects.create(
        title="🚨 RACE TEST - 1 SPOT",
        description="Race condition testing",
        category=category,
        date=timezone.now() + timezone.timedelta(days=1),
        location="Test",
        organizer=user,
        max_attendees=1
    )
    return event.id

def test_user(event_id, user_num, results):
    client = APIClient()
    user = User.objects.get(username='preetham')
    client.force_authenticate(user=user)
    
    response = client.post(f'/events/api/events/{event_id}/register/')
    
    if response.status_code == 201:
        results.append(f"User {user_num}: ✅ SUCCESS")
    else:
        results.append(f"User {user_num}: ❌ FAILED")

def run_test():
    print("🔥 RACE CONDITION TEST")
    print("=" * 40)
    
    event_id = create_test_event()
    Registration.objects.filter(event_id=event_id).delete()
    
    threads = []
    results = []
    
    print("Testing 3 users → 1 spot...")
    
    for i in range(3):
        thread = threading.Thread(target=test_user, args=(event_id, i+1, results))
        threads.append(thread)
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("\n📊 RESULTS:")
    for result in results:
        print(f"  {result}")
    
    event = Event.objects.get(id=event_id)
    print(f"\nFinal: {event.registered_count}/1 registrations")
    
    if event.registered_count == 1:
        print("🎉 RACE CONDITION FIXED!")
    else:
        print("💥 RACE CONDITION EXISTS!")
    
    event.delete()
    print("Test cleaned up")

if __name__ == "__main__":
    run_test()