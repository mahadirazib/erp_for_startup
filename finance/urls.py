from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.seeSalary , name='see_salary'),
    path('see_salaries_in_details/', views.seeSalaryInDetails , name='see_salaries_in_details'),
    path('update_salary/', views.updateSalary , name='update_salary'),
    path('create_monthly_salary/', views.createSelaryStatus , name='create_monthly_salary'),
    path('make_employee_salary_paid/<int:id>', views.makeEmployeeSalaryPaid , name='make_employee_salary_paid'),
    path('accounts/', views.accountsMainView , name='accounts'),
    path('accounts_spend_money/', views.addSpendMoney , name='accounts_spend_money'),
    path('edit_spend_entry/<int:id>', views.editSpendMoney , name='edit_spend_entry'),
    path('edit_recived_entry/<int:id>', views.editRecivedMoney , name='edit_recived_entry'),
    path('delete_spend_entry/<int:id>', views.deleteSpendMoney , name='delete_spend_entry'),
    path('delete_recived_entry/<int:id>', views.deleteRecivedMoney , name='delete_recived_entry'),
    path('entity_register/', views.registerEntity , name='entity_register'),
    path('see_entity_to_edit/', views.seeAllEntry , name='see_entity_to_edit'),
    path('entity_edit/<int:id>', views.editEntity , name='entity_edit'),
    
]