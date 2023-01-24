from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from datetime import date
from django.db.models import Count, Q
from anki_web.decks.models import Decks


class MainPageView(ListView):
    model = Decks
    template_name = 'main_page.html'
    context_object_name = 'decks'

    def get_queryset(self):
        new = Count('cards', filter=Q(cards__review_date__isnull=True))
        old = Count('cards', filter=Q(cards__review_date__lte=date.today()))
        cards = Count('cards')
        queryset = self.model._default_manager.filter(
            created_by=self.request.user.id
        ).values(
            'id', 'name'
        ).annotate(new_cards=new).annotate(old_cards=old).annotate(all_cards=cards).filter(all_cards__gt=0)
        return queryset


class LoginUserView(LoginView):
    template_name = 'login.html'
