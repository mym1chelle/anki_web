from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from .models import Decks
from anki_web.users.models import Users
from .forms import CreateDeskForm
from anki_web.custom_mixins.mixins import CheckConnectMixin
from django.db.models import Count


class ListDecksView(ListView):
    model = Decks
    template_name = 'decks/decks.html'
    context_object_name = 'decks'


class CreateDeckView(SuccessMessageMixin, CreateView):
    model = Decks
    form_class = CreateDeskForm
    template_name = 'form.html'
    success_url = reverse_lazy('decks:decks')
    success_message = 'Колода успешно создана'

    def form_valid(self, form):
        form.instance.created_by = Users.objects.get(pk=self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Добавить'
        return context


class DeleteDeckView(SuccessMessageMixin, CheckConnectMixin, DeleteView):
    model = Decks
    template_name = 'delete.html'
    success_url = reverse_lazy('decks:decks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Удалить все'
        return context
