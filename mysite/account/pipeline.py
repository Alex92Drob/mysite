from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Profile

def save_profile(backend, strategy, details, response, user=None, *args, **kwargs):
    if user:
        try:
            Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            Profile.objects.create(user=user)