from django.urls import path
from .views import contact, verify_contact

urlpatterns = [
    path('', contact, name='contact'),  # URL for the contact page
    path('verify-contact/', verify_contact, name='verify_contact'),  # URL for the verification page
]
