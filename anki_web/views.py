from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from datetime import date
from django.db.models import Count
from anki_web.decks.models import Decks


class MainPageView(ListView):
    model = Decks
    template_name = 'main_page.html'
    context_object_name = 'decks'

    def get_queryset(self):
        if self.model is not None:
            decks = self.model._default_manager.all()
            queryset = [{
                    'id': deck.id,
                    'name': deck.name,
                    'new_cards': deck.cards_set.filter(review_date__isnull=True).aggregate(count=Count('question')),
                    'old_cards': deck.cards_set.filter(review_date__lte=date.today()).aggregate(count=Count('question'))
            } for deck in decks]
            return queryset


class LoginUserView(LoginView):
    template_name = 'login.html'
