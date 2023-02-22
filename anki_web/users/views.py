from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import Users
from .forms import CreateUserForm, UpdateUserForm


class CreateUserView(generic.CreateView):
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


class UpdateUserInfoView(generic.UpdateView):
    model = Users
    form_class = UpdateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('show_user')
    success_message = 'Пользователь был успешно обновлен'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Обновить'
        return context


def change_password(request):
    if request.method == 'GET':
        form = PasswordChangeForm(user=request.user)
        return render(
            request,
            template_name='form.html',
            context={
                'form': form,
                'text_button': 'Изменить пароль'
            }
        )
    elif request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request, 'Пароль успешно изменен')
            return redirect('login')
        else:
            print('invalid')
            print(form.errors)
            return render(request, 'form.html', {'form': form})
