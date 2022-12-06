from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    model = CustomUser
    success_url = reverse_lazy('main:home')
    template_name = 'registration/signup.html'
