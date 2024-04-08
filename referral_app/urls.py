from django.urls import path
from .views import user_registration, user_details, referrals
urlpatterns = [
 path('register/', user_registration, name='user-registration'),
 path('details/', user_details, name='user-details'),
 path('referrals/', referrals, name='user-referrals'),
]