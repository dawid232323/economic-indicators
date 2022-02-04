from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User

from . import forms
from . import models


TIME_PERIODS = {
    1: "Poprzedni okres obrachunkowy (x-3)",
    2: "Poprzedni okres obrachunkowy (x-2)",
    3: "Ostatni okres obrachunkowy (x-1)",
    4: 'Okres bieżący (x)',
    5: 'Prognoza na koniec okresu (x)',
    6: 'Prognoza na koniec kolejnego roku (x+1)',
    7: 'Prognoza na koniec kolejnego roku (x+2)',
    8: 'Prognoza na koniec kolejnego roku (x+3)'
}


class RegisterView(FormView):
    form_class = forms.UserRegisterForm
    template_name = 'economic_indicators_site/authentication/register_page.html'
    success_url = '/login'

    def form_valid(self, form):
        new_form = form.save()
        return super().form_valid(form)


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'economic_indicators_site/authentication/login_page.html'
    next_page = '/home'

    def form_valid(self, form):
        print(form.cleaned_data.get('username'))
        try:
            username = str(form.cleaned_data.get('username'))
            logged_user = User.objects.get(username=username)
            if not models.CompanySystemUser.objects.filter(user_id=logged_user.id).exists():
                self.next_page = f'choose_company/?username={username}'
            else:
                self.next_page = f'/home'
        except Exception as ex:
            logged_user = None
        finally:
            return super().form_valid(form)


class AddCompanySystemUserView(LoginRequiredMixin, CreateView):
    form_class = forms.AddUserCompanyForm
    template_name = 'economic_indicators_site/authentication/register_page.html'
    success_url = '/home'
    login_url = '/login'
    redirect_field_name = ''

    def get(self, request, *args, **kwargs):
        if models.CompanySystemUser.objects.filter(user__username=request.user.username).exists():
            return HttpResponseRedirect('/home')
        return super(AddCompanySystemUserView, self).get(request, *args, **kwargs)

#TODO
# Add custom error page that will tell the user that he cannot choose anyone but himself
    def form_valid(self, form):
        username = str(self.request.GET.get('username'))
        current_user = User.objects.get(username=username).username.replace(' ', '')
        cleaned_username = str(form.cleaned_data['user']).replace(' ', '')
        if cleaned_username != current_user:
            raise Exception
        else:
            return super(AddCompanySystemUserView, self).form_valid(form)


class RegisterNewUserView(SuccessMessageMixin, CreateView):
    form_class = forms.TestRegisterForm
    template_name = 'economic_indicators_site/authentication/register_page.html'
    success_url = '/login'
    success_message = 'User Created successfully'


class LogOutUser(LogoutView):
    next_page = '/login'
    template_name = 'economic_indicators_site/authentication/login_page.html'


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'economic_indicators_site/homePage.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_system_user = models.CompanySystemUser.objects.get(user__username=self.request.user.username)
        context['username'] = self.request.user.username
        # context['raports'] = models.FullRaport.objects.filter(company_id=current_system_user.company.id)
        return context


class CreateNewRaportBlockView(FormView):
    template_name = 'economic_indicators_site/forms/basicForm.html'
    page_title = 'Uzupełnij'

    def form_valid(self, form): #Here developer needs to fill the success_url
        form.cleaned_data['user'] = self.request.user
        form.cleaned_data['time_period'] = int(self.request.GET.get('number'))
        form.save()
        return super(CreateNewRaportBlockView, self).form_valid(form)

    def get_context_data(self, **kwargs): # Here user has to fill the page_title
        context = super(CreateNewRaportBlockView, self).get_context_data(**kwargs)
        context['subject'] = self.page_title
        return context

class CreateFixedAssetsView(LoginRequiredMixin, CreateNewRaportBlockView):
    form_class = forms.AddFixedAssetsForm
    login_url = '/login'
    success_url = '/new_raport/fixed_assets/'
    page_title = 'Uzupełnij Aktywa trwałe za '

    def form_valid(self, form):
        time_number = int(self.request.GET.get('number'))
        if time_number == 8:
            self.success_url = '/new_raport/current_assets/?number=1'
        else:
            self.success_url = f'/new_raport/fixed_assets/?number={time_number + 1}'
        return super(CreateFixedAssetsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        period = TIME_PERIODS[int(self.request.GET.get('number'))]
        self.page_title = f'Uzupełnij aktywa trwałe za {period}'
        return super(CreateFixedAssetsView, self).get_context_data()


class CreateCurrentAssetsView(LoginRequiredMixin, CreateNewRaportBlockView):
    template_name = 'economic_indicators_site/forms/basicForm.html'
    form_class = forms.AddCurrentAssetsForm
    login_url = '/login'
    success_url = '/new_raport/current_assets/'

    def form_valid(self, form):
        time_number = int(self.request.GET.get('number'))
        if time_number == 8:
            self.success_url = '/new_raport/liabilities_provisions/?number=1'
        else:
            self.success_url = f'/new_raport/current_assets/?number={time_number + 1}'
        return super(CreateCurrentAssetsView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        period = TIME_PERIODS[int(self.request.GET.get('number'))]
        self.page_title = f'Uzupełnij aktywa obrotowe za {period}'
        return super(CreateCurrentAssetsView, self).get_context_data(**kwargs)

