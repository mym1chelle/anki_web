from anki_web.users.forms import LoginUserForm
from anki_web.decks.models import Decks
from anki_web.users.models import Users
from django.db.models import Count, Q
from datetime import date
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordContextMixin
)
from anki_web.forms import CustomResetPasswordForm
from anki_web.custom_mixins.mixins import NotLoginRequiredMixin


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
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Изменить пароль'
        return context

class ResetPasswordCompleteView(NotLoginRequiredMixin, PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Пароль был успешно изменен')
        return redirect(reverse_lazy('login'))


class ResetPasswordDoneView(NotLoginRequiredMixin, PasswordContextMixin, TemplateView):
    template_name = "users/info_message.html"
    title = "Письмо с инструкциями по восстановлению пароля отправлено"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_text'] = """
        Мы отправили вам инструкцию по установке нового пароля на указанный адрес электронной почты (если в нашей базе данных есть такой адрес). Вы должны получить ее в ближайшее время.
        Если вы не получили письмо, пожалуйста, убедитесь, что вы ввели адрес с которым Вы зарегистрировались, и проверьте папку со спамом.
        """
        return context
