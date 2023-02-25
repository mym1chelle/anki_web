from anki_web.users.forms import LoginUserForm
from anki_web.decks.models import Decks
from anki_web.users.models import Users
from django.db.models import Count, Q
from datetime import date
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView
)
from anki_web.forms import CustomResetPasswordForm
from anki_web.mixins.castom_mixins import NotLoginRequiredMixin


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
        ).annotate(new_cards=new).annotate(old_cards=old).annotate(
            all_cards=cards).filter(all_cards__gt=0)
        return queryset


class LoginUserView(LoginView):
    template_name = 'login.html'
    form_class = LoginUserForm
    redirect_authenticated_user = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Вход'
        return context


class ResetPasswordView(NotLoginRequiredMixin, PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'users/reset_password_mail.html'
    form_class = CustomResetPasswordForm
    template_name = 'form.html'
    text_button = 'Сбросить пароль'

    def post(self, request, *args: str, **kwargs):
        mail = request.POST.get('email')
        try:
            Users.objects.get(email=mail)
            return super().post(request, *args, **kwargs)
        except ObjectDoesNotExist:
            messages.error(self.request, f'Адрес {mail} не зарегистрирован')
            return render(
                request,
                template_name=self.template_name,
                context={
                    'form': self.form_class,
                    'text_button': self.text_button,
                    'help_text': """Забыли пароль? Введите свой адрес электронной почты ниже, и мы вышлем вам инструкцию, как установить новый пароль."""
                }
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = self.text_button
        context['help_text'] = """Забыли пароль? Введите свой адрес электронной почты ниже, и мы вышлем вам инструкцию, как установить новый пароль."""
        return context


class ResetPasswordConfirmView(NotLoginRequiredMixin, PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')


class ResetPasswordCompleteView(NotLoginRequiredMixin, PasswordResetCompleteView):
    pass


class ResetPasswordDoneView(NotLoginRequiredMixin, PasswordResetDoneView):
    pass
