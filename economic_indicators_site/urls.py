from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterNewUserView.as_view()),
    path('login/', views.LoginUserView.as_view()),
    path('login/choose_company/', views.AddCompanySystemUserView.as_view()),
    path('home', views.HomePageView.as_view()),
    path('logout', views.LogOutUser.as_view()),
    path('new_raport/fixed_assets/', views.CreateFixedAssetsView.as_view()),
    path('new_raport/current_assets/', views.CreateCurrentAssetsView.as_view())
]
