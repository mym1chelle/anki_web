from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class CheckConnectMixin(AccessMixin):
    def form_valid(self, form):
        """Check if any other objects are linked to the given object."""
        result = self.object.cards_set.all()
        if result:
            messages.error(self.request, 'Нельзя удалить не пустую колоду')
        else:
            self.object.delete()
            messages.success(self.request, 'Колода успешно удалена')
        return redirect(self.get_success_url())
