from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm

def home(request):
    return render(request, 'model/home.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "User registered successfully! You can now login.")
        return redirect('login')

    return render(request, 'model/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'model/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

def services(request):
    return render(request, 'model/services.html')

def about(request):
    return render(request, 'model/about.html')

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_protect, name='dispatch')
class ContactFormView(FormView):
    template_name = 'model/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact-success')

    def form_valid(self, form):
        response = super().form_valid(form)  # ✅ keeps Django’s CSRF flow intact
        return render(self.request, 'model/contact_success.html', {'data': form.cleaned_data})

    

from events.models import Event, Registration  

def home(request):
    context = {}
    if request.user.is_authenticated:
        # ADD THESE LINES:
        context['organized_count'] = Event.objects.filter(organizer=request.user).count()
        context['attending_count'] = Registration.objects.filter(user=request.user).count()
    return render(request, 'model/home.html', context)