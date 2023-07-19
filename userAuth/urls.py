from django.urls import path
from . import views
from dashboard import views as dviews


app_name = 'userAuth'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', dviews.dashboardMainView, name='dashboard'),
    path('register/', views.userRegistration, name='userRegistation'),
    path('employee_delete/<int:id>', views.employeeDelete, name='employee_delete'),
    path('login/', views.loginApp, name='loginApp'),
    path('logout/', views.logoutApp, name='logoutApp'),
]

