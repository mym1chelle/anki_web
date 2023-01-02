from django.contrib.auth.mixins import AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView,\
    ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import Users
from .forms import CreateUserForm


class CreateUserView(CreateView):
    model = Users
    form_class = CreateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
