#  Create my mixins
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class NotLoginRequiredMixin(AccessMixin):
    """Verify that the current user is not authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Вы авторизированы')
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)
