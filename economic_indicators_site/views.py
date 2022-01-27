from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView

from . import forms


class RegisterView(FormView):
    form_class = forms.UserRegisterForm
    template_name = 'economic_indicators_site/register_page.html'
    success_url = '/login'

    def form_valid(self, form):
        new_form = form.save()
        return super().form_valid(form)


class LoginView(FormView):
    form_class = forms.LoginUserForm
    template_name = 'economic_indicators_site/login_page.html'
    success_url = 'home'

    # TODO Create login authenticaion
    def form_valid(self, form):
        return super().form_valid(form)
