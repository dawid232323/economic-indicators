from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterNewUserView.as_view()),
    path('login/', views.LoginUserView.as_view()),
    path('login/choose_company/', views.AddCompanySystemUserView.as_view()),
    path('home', views.HomePageView.as_view()),
    path('logout', views.LogOutUser.as_view()),
    path('new_raport/add_assets/', views.AddNewAssetsView.as_view()),
    path('new_raport/add_liabilities/', views.AdddNewLiabilitiesView.as_view()),
    path('new_raport/add_profits_loses/', views.AddNewProfitsLosesView.as_view()),
]
