from django.shortcuts import render
from django.db.models import Q

from userAuth import models
from .models import salary, paidUnpaidSalaryStatus, clientAndServiceProvider, recivedMoney, spendMoney

from . import forms

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

import datetime

# Create your views here.


@login_required
def seeSalary(request):
    
    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk=currentUser.id)

    dict = {}

    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "2" or currentUserMoreInfo.role == "3" ):
        dict.update({"employeeController": True})

    if (currentUserMoreInfo.role == "1"):
        dict.update({"fullEmployeeControler": True})

    if currentUserMoreInfo.role == '1' or currentUserMoreInfo.role == '4':

        salaryAndUser = models.User.objects.values( 'id', 'first_name', 'last_name', 'userinfo__role', 'salary__salary', 'salary__id').order_by('userinfo__role')
        dict.update({"finaceController": True})
        dict.update({'salaryAndUser': salaryAndUser})


    return render(request, 'finance/seeSalary.html', context=dict)




@login_required
def seeSalaryInDetails(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk=currentUser.id)

    dict = {}

    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "2" or currentUserMoreInfo.role == "3" ):
        dict.update({"employeeController": True})

    if (currentUserMoreInfo.role == "1"):
        dict.update({"fullEmployeeControler": True})


    if currentUserMoreInfo.role == '1' or currentUserMoreInfo.role == '4':

        user = models.User.objects.all()

        salaryAndUser = paidUnpaidSalaryStatus.objects.all()

        dict.update({"finaceController": True})
        dict.update({'salaryAndUser': salaryAndUser})

    return render(request, 'finance/employeeSalaries.html', context=dict)




@login_required
def updateSalary(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):
        if request.method == "POST":

            employeeId = request.POST.get("id")
            salaryId = request.POST.get("salaryid")
            employeeSalary = request.POST.get("salary")

            employee = models.User.objects.get(pk=employeeId)

            if salary.objects.filter(user=employee):
                newSalary = salary.objects.get(user=employee)
                newSalary.salary = employeeSalary
                newSalary.save()
            else:
                newSalary = salary(user=employee, salary=employeeSalary)
                newSalary.save()

    return HttpResponseRedirect(reverse('finance:see_salary'))
    
    


@login_required
def createSelaryStatus(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    dict = {}

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):
        dict.update({"finaceController": True})

        today = datetime.datetime.now()

        startDate = datetime.datetime(today.year, today.month, 1)
        endDate = ''
        if (today.month==2):
            endDate = datetime.datetime(today.year, today.month, 28)
        elif (today.month == 4) or (today.month == 6) or (today.month == 9) or (today.month == 11):
            endDate = datetime.datetime(today.year, today.month, 30)
        else:
            endDate = datetime.datetime(today.year, today.month, 31)


        monthlySelary = paidUnpaidSalaryStatus.objects.filter(month__range=[startDate, endDate])
        monthlySelaryCount = monthlySelary.count()


        userWithRole = models.userInfo.objects.all()
        userWithRoleCount = userWithRole.count()

        checking = True

        for salaryInMonth in monthlySelary:
            employeePayable = salary.objects.get(user=salaryInMonth.user)

            if salaryInMonth.monthlySalary!=employeePayable.salary:
                salaryInMonth.monthlySalary = employeePayable.salary
                salaryInMonth.paidStatus = False
                salaryInMonth.save()
                checking = False


        if monthlySelaryCount and checking:
            dict.update({'message': 'Already Created.You can not pay the employeese that joined in this month.'})
            return render(request, 'showMessage.html', context=dict)

        if monthlySelaryCount and (checking==False):
            dict.update({'message': 'Salary Sheet successfully updated.'})
            return render(request, 'showMessage.html', context=dict)


        monthlySalaryAndUser = models.User.objects.values( 'id', 'first_name', 'last_name', 'userinfo__role', 'salary__salary', 'salary__id').order_by('userinfo__role')

        for user in monthlySalaryAndUser:



            if(user['userinfo__role']):

                employee = models.User.objects.get(pk=user['id'])
                employeeSalary = user['salary__salary']

                newSalaryEntry = paidUnpaidSalaryStatus(user=employee)
                newSalaryEntry.monthlySalary = employeeSalary
                newSalaryEntry.month = datetime.datetime.now()
                newSalaryEntry.paidStatus = False
                newSalaryEntry.save()


        dict.update({'message': 'Salary Sheet created successfully.'})
        dict.update({"finaceController": True})
        return render(request, 'showMessage.html', context=dict)



    dict = {'message': 'You are not from finance'}
    return render(request, 'showMessage.html', context=dict)



@login_required
def makeEmployeeSalaryPaid(request, id):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):

        monthlyEmployeeSelary = paidUnpaidSalaryStatus.objects.get(pk=id)
        monthlyEmployeeSelary.paidStatus = True
        monthlyEmployeeSelary.save()

        return HttpResponseRedirect(reverse('finance:see_salaries_in_details'))


    dict = {'message': 'You are not from finance'}
    return render(request, 'showMessage.html', context=dict)











@login_required
def accountsMainView(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):
        dict = {'finaceController': True}
        recivedAmount = 0
        spendAmount = 0

        recivedEntries = ''
        spendEntries = ''
        
        recivedEntries = recivedMoney.objects.all().order_by('-date')
        dict.update({'recivedEntries': recivedEntries})

        for money in recivedEntries:
            recivedAmount += money.amount

        spendEntries = spendMoney.objects.all().order_by('-date')
        dict.update({'spendEntries': spendEntries})

        for money in spendEntries:
            spendAmount += money.amount

        currentBalance = recivedAmount-spendAmount


        searchName = request.GET.get('name')
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')

        if (searchName and startDate and endDate) or (searchName and startDate) or (searchName and endDate):
            if not endDate:
                endDate = datetime.datetime.now()

            if not startDate:
                startDate = datetime.datetime(2000, 1, 1)

            recivedEntries = recivedMoney.objects.filter(Q(recivedFrom__name__icontains=searchName) | Q(recivedFrom__email__icontains=searchName) | Q(recivedFrom__companyName__icontains=searchName)).filter(date__range=[startDate, endDate]).order_by('-date')
            recivedAmount = 0
            for money in recivedEntries:
                recivedAmount += money.amount

            spendEntries = spendMoney.objects.filter(Q(spendOn__name__icontains=searchName) | Q(spendOn__email__icontains=searchName) | Q(spendOn__companyName__icontains=searchName)).filter(date__range=[startDate, endDate]).order_by('-date')
            spendAmount = 0
            for money in spendEntries:
                spendAmount += money.amount

        elif searchName:
            recivedEntries = recivedMoney.objects.filter(Q(recivedFrom__name__icontains=searchName) | Q(recivedFrom__email__icontains=searchName) | Q(recivedFrom__companyName__icontains=searchName)).order_by('-date')
            recivedAmount = 0
            for money in recivedEntries:
                recivedAmount += money.amount

            spendEntries = spendMoney.objects.filter(Q(spendOn__name__icontains=searchName) | Q(spendOn__email__icontains=searchName) | Q(spendOn__companyName__icontains=searchName)).order_by('-date')
            spendAmount = 0
            for money in spendEntries:
                spendAmount += money.amount

        elif startDate and endDate:
            recivedEntries = recivedMoney.objects.filter(date__range=[startDate, endDate]).order_by('-date')
            recivedAmount = 0
            for money in recivedEntries:
                recivedAmount += money.amount

            spendEntries = spendMoney.objects.filter(date__range=[startDate, endDate]).order_by('-date')
            spendAmount = 0
            for money in spendEntries:
                spendAmount += money.amount

        elif startDate:
            endDate = datetime.datetime.now()
            recivedEntries = recivedMoney.objects.filter(date__range=[startDate, endDate]).order_by('-date')
            recivedAmount = 0
            for money in recivedEntries:
                recivedAmount += money.amount

            spendEntries = spendMoney.objects.filter(date__range=[startDate, endDate]).order_by('-date')
            spendAmount = 0
            for money in spendEntries:
                spendAmount += money.amount

        else:

            today = datetime.datetime.now()
            thisYearstart = datetime.datetime(today.year, 1, 1)

            recivedEntries = recivedMoney.objects.filter(date__range=[thisYearstart, today]).order_by('-date')
            dict.update({'recivedEntries': recivedEntries})

            for money in recivedEntries:
                recivedAmount += money.amount

            spendEntries = spendMoney.objects.filter(date__range=[thisYearstart, today]).order_by('-date')
            dict.update({'spendEntries': spendEntries})

            for money in spendEntries:
                spendAmount += money.amount

            currentBalance = recivedAmount-spendAmount

        dict.update({'spendEntries': spendEntries})
        dict.update({'recivedEntries': recivedEntries})
        dict.update({'currentBalance': currentBalance})
        dict.update({'recivedAmount': recivedAmount})
        dict.update({'spendAmount': spendAmount})

        clients = clientAndServiceProvider.objects.all()
        dict.update({'clients': clients})

        if request.method == 'POST':

            userid = request.POST.get("user")
            user = clientAndServiceProvider.objects.get(pk=userid)
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            purpose = request.POST.get("purpose")
            medium = request.POST.get("medium")

            newEntry = recivedMoney(recivedFrom=user)
            newEntry.amount = amount
            newEntry.date = date
            newEntry.purpose = purpose
            newEntry.medium = medium

            newEntry.save()

            dict = {'message': "Successfully added.", 'finaceController': True}
            return render(request, 'showMessage.html', context=dict)
            

        return render(request, 'finance/accountsMain.html', context=dict)
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)



@login_required
def addSpendMoney(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):

        if request.method == 'POST':

            userid = request.POST.get("user")
            user = clientAndServiceProvider.objects.get(pk=userid)
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            purpose = request.POST.get("purpose")
            medium = request.POST.get("medium")

            newEntry = spendMoney(spendOn=user)
            newEntry.amount = amount
            newEntry.date = date
            newEntry.purpose = purpose
            newEntry.medium = medium

            newEntry.save()
            

        return HttpResponseRedirect(reverse('finance:accounts'))
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)



@login_required
def editSpendMoney(request, id):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):

        spendMoneyEntry = spendMoney.objects.get(pk=id)
        spendMoneyUserId = spendMoneyEntry.spendOn.id
        users = clientAndServiceProvider.objects.all()
        dict = {'entry': spendMoneyEntry, 'clients': users, 'selectedClient': spendMoneyUserId, 'finaceController': True, 'spend': True}


        if request.method == 'POST':

            date = request.POST.get("date")
            amount = request.POST.get("amount")
            userid = request.POST.get("user")
            user = clientAndServiceProvider.objects.get(pk=userid)
            purpose = request.POST.get("purpose")
            medium = request.POST.get("medium")

            newEntry = spendMoney.objects.get(pk=id)
            newEntry.spendOn = user
            newEntry.date = date
            newEntry.amount = amount
            newEntry.purpose = purpose
            newEntry.medium = medium

            newEntry.save()
            return HttpResponseRedirect(reverse('finance:accounts'))

        return render(request, 'finance/editEntries.html', context=dict)
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)




@login_required
def editRecivedMoney(request, id):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):

        recivedMoneyEntry = recivedMoney.objects.get(pk=id)
        recivedMoneyUserId = recivedMoneyEntry.recivedFrom.id
        users = clientAndServiceProvider.objects.all()
        dict = {'entry': recivedMoneyEntry, 'clients': users, 'selectedClient': recivedMoneyUserId, 'finaceController': True, 'spend': False}


        if request.method == 'POST':

            date = request.POST.get("date")
            amount = request.POST.get("amount")
            userid = request.POST.get("user")
            user = clientAndServiceProvider.objects.get(pk=userid)
            purpose = request.POST.get("purpose")
            medium = request.POST.get("medium")

            newEntry = recivedMoney.objects.get(pk=id)
            newEntry.recivedFrom = user
            newEntry.date = date
            newEntry.amount = amount
            newEntry.purpose = purpose
            newEntry.medium = medium

            newEntry.save()
            return HttpResponseRedirect(reverse('finance:accounts'))

        return render(request, 'finance/editEntries.html', context=dict)
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)




@login_required
def deleteSpendMoney(request, id):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):

        spendMoneyEntry = spendMoney.objects.get(pk=id)
        spendMoneyEntry.delete()
   
        return HttpResponseRedirect(reverse('finance:accounts'))
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)



@login_required
def deleteRecivedMoney(request, id):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):

        recivedMoneyEntry = recivedMoney.objects.get(pk=id)
        recivedMoneyEntry.delete()
   
        return HttpResponseRedirect(reverse('finance:accounts'))
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)







@login_required
def registerEntity(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):

        
        entityForm = forms.registerEntity

        dict = {'entityForm': entityForm, 'finaceController': True}

        if request.method == 'POST':

            formData = forms.registerEntity(data=request.POST)

            if formData.is_valid():
                formData.save()
                return HttpResponseRedirect(reverse('finance:accounts'))
            
            dict.update({'message':"Something went wrong. try again"})


        return render(request, 'finance/entityRegistration.html', context=dict)
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)



@login_required
def seeAllEntry(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):
        dict = {'finaceController': True}

        entries = clientAndServiceProvider.objects.all()
        dict.update({'entryList': entries})

        return render(request, 'finance/seeEntityToEdit.html', context=dict)
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)


@login_required
def editEntity(request, id):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == '1') or (currentUserMoreInfo.role == '4'):

        instanceEntity = clientAndServiceProvider.objects.get(pk=id)
        entityForm = forms.registerEntity(instance=instanceEntity)

        dict = {'entityForm': entityForm, 'finaceController': True, 'editText': 'Edit Entity'}

        if request.method == 'POST':

            formData = forms.registerEntity(request.POST, instance=instanceEntity)

            if formData.is_valid():
                formData.save()
                return HttpResponseRedirect(reverse('finance:accounts'))
            
            dict.update({'message':"Something went wrong. try again"})

        return render(request, 'finance/entityRegistration.html', context=dict)
    
    dict = {'message': 'You do not have the authority to see this page.'}
    return render(request, 'showMessage.html', context=dict)










