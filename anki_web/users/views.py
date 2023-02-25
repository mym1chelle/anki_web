from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Users
from .forms import CreateUserForm, UpdateUserForm, ChangePasswordForm, AddEmailForm


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
        form = ChangePasswordForm(user=request.user)
        return render(
            request,
            template_name='form.html',
            context={
                'form': form,
                'text_button': 'Изменить пароль'
            }
        )
    elif request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request, 'Пароль успешно изменен')
            return redirect('login')
        else:
            print('invalid')
            print(form.errors)
            return render(request, 'form.html', {
                'form': form,
                'text_button': 'Изменить пароль'
            })


class AddEmailView(generic.UpdateView):
    model = Users
    form_class = AddEmailForm
    template_name = 'form.html'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        new_email = self.request.POST.get('email')
        if self.request.user.email == new_email and self.request.user.email_is_active:
            messages.info(self.request, message=f'Почта {new_email} уже подтверждена')
            return redirect(reverse_lazy('add_email', kwargs={'pk': self.object.id}))
        user = form.save(commit=False)
        user.email_is_active = False
        user.save()
        
        current_site = get_current_site(self.request)
        mail_subject = 'Activation link has been sent to your email id'
        mail_body = render_to_string('users/confirm_email.html',
                                     {
                                         'user': self.object,
                                         'domain': current_site.domain,
                                         'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
                                         'token': default_token_generator.make_token(user=self.object)
                                     })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, mail_body, to=[to_email]
        )
        email.send()
        messages.info(self.request, message='Please confirm your email address to complete the registration')
        return redirect('show_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.email:
            context['text_button'] = 'Обновить'
        else:
            context['text_button'] = 'Добавить почту'
        return context


def activate_email(request, uidb64, token):  
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = Users.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    print(default_token_generator.check_token(user, token))
    if user is not None and default_token_generator.check_token(user, token):
        user.email_is_active = True
        user.save()
        messages.success(request, message='Thank you for your email confirmation. Now you can login your account.')
        return redirect('show_user')
    else:
        messages.error(request, message='Activation link is invalid!')
        return redirect('show_user')