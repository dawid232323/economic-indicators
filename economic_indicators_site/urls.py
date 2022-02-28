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
    path('generate_raport/', views.GenerateRaportView.as_view()),
    path('full_raport_view/', views.FullRaportView.as_view()),
    path('generate_raport_file/', views.GenerateRaportFileView.as_view()),
    path('add_business_characteristic/', views.BusinessCharacteristicView.as_view()),
    path('add_type_economic_activity', views.TypeOfEconomicActivityView.as_view()),
    path('add_applicant_op_income', views.ApplicantOfferOpeartionIncomeView.as_view()),
    path('add_curent_place_on_market', views.CurrentPlaceOnTheMarketView.as_view()),
    path('generate_market_analisis_raport', views.GenerateMarketAnalysisRaport.as_view()),
    path('raport_analysis/<int:id>', views.MarketAnalysisView.as_view()),
    path('generate_market_analysis/<int:id>', views.GenerateMarketAnalysisFileView.as_view()),
    path('add_third_a1/', views.AddA1ThirdModuleView.as_view()),
    path('add_third_a2/', views.AddA2ThirdModuleView.as_view()),
    path('add_third_a3/', views.AddA3ThirdModuleView.as_view()),
    path('add_third_a4/', views.AddA4ThirdModuleView.as_view()),
    path('add_third_a5/', views.AddA5ThirdModuleView.as_view()),
    path('add_third_a6/', views.AddA6ThirdModuleView.as_view()),
    path('add_third_a7/', views.AddA7ThirdModuleView.as_view()),
    path('add_third_a8/', views.AddA8ThirdModuleView.as_view()),
    path('add_third_a9/', views.AddA9ThirdModuleView.as_view()),
    path('add_third_a10/', views.AddA10ThirdModuleView.as_view()),
    path('generate_third_module_raport/', views.GenerateThirdModuleRaport.as_view()),
    path('third_module_raport/<int:id>', views.ThirdModuleRaportView.as_view()),
    path('generate_third_module_file/<int:id>', views.GenerateThirdModuleFileView.as_view())
]
