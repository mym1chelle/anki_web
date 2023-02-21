from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Users
from .forms import CreateUserForm


class CreateUserView(CreateView):
    model = Users
    form_class = CreateUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Зарегистрироваться'
        return context


@login_required
def show_user(request):
    username = request.user.username
    date_joined = request.user.date_joined
    cards = request.user.cards_set.count()
    decks = request.user.decks_set.count()
    return render(
        request,
        'users/profile.html',
        context={
            'username': username,
            'date_joined': date_joined,
            'cards': cards,
            'decks': decks
        }
    )
