from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.template import loader
from django.core.mail import EmailMultiAlternatives


class CustomResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label='Эл. почта',
        max_length=254,
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            'class': 't-text-gray-900 sm:t-text-sm t-rounded-lg t-block t-w-full t-p-2.5',
            'placeholder': 'Эл.почта'
        }),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = 'sex'
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(
                html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()
