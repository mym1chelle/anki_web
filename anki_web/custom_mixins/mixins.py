from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


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


class NotLoginRequiredMixin(AccessMixin):
    """Verify that the current user is not authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Вы авторизированы')
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)
