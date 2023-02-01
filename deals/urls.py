from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.dealsMainView , name='deals'),
    path('old_deals/', views.oldDeals , name='old_deals'),
    path('register_new_deal/', views.registerNewDeal , name='register_new_deal'),
    path('edit_deals/<int:id>/', views.editDeal , name='edit_deals'),
    path('terminate_or_end_deals/<int:id>/<str:endOrTerminate>/', views.terminateOrEndDeals , name='terminate_or_end_deals'),
    
]