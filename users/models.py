from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    pass

    def get_absolute_url(self):
        return reverse('account:update', args=[self.request.user])
