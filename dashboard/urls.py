from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboardMainView , name='dashboard'),
    path('edit_profile/<int:id>/', views.editProfile , name='edit_profile'),
    path('createNotice/', views.createNotice , name='createNotice'),
    path('edit_notice/<int:id>/', views.editNotice , name='edit_notice'),
    path('make_complete/<int:id>/', views.makeComplete , name='make_complete'),
    path('make_incomplete/<int:id>/', views.makeIncomplete , name='make_incomplete'),
    path('delete_notice/<int:id>/', views.deleteNotice , name='delete_notice'),
    path('seeAllEmployee/', views.seeAllEmployee , name='seeAllEmployee'),
]
