from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('contact/success/', TemplateView.as_view(template_name='model/contact_success.html'), name='contact-success'),
]