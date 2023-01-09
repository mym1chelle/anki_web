from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Users
from .forms import CreateUserForm


class CreateUserView(CreateView):
    model = Users
    form_class = CreateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
