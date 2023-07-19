from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from dashboard.views import dashboardMainView

from .forms import userform, userformMoreinfo
from .models import userInfo, User
from . import models


def index(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    else:
        return HttpResponseRedirect(reverse('userAuth:loginApp'))




def notFound(request, exception):
    dict = {'message': 'Page Not Found'}
    return render(request, 'showMessage.html', context=dict)



@login_required
def userRegistration(request):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)
    currentRole = currentUserMoreInfo.role

    if (currentRole != '1') and (currentRole !='2') and (currentRole != '3'):
        dict={'showMessage': True,'message': "You can not add any employee"}
        return render(request, 'showMessage.html', context=dict)


    userForm = userform
    userForm2 = userformMoreinfo
    dict = {'userform': userForm, 'userform2': userForm2}


    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "2" or currentUserMoreInfo.role == "3" ):
        dict.update({"employeeController": True})

    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "4" ):
        dict.update({"finaceController": True})
    
    if (currentUserMoreInfo.role == "1"):
        dict.update({"fullEmployeeControler": True})


    if request.method == 'POST':

        userForm = userform(data=request.POST)
        userInfoForm = userformMoreinfo(data=request.POST)


        if userForm.is_valid() and userInfoForm.is_valid():

            givenRole = userInfoForm.cleaned_data['role']

            if (givenRole == '1') and (currentRole != '1'):
                dict={'showMessage': True,'message': "You can not add Chief. Only Cheif can add another chief"}
                return render(request, 'showMessage.html', context=dict)
            
    
            if (currentRole != '1') and (currentRole !='2') and (currentRole != '3'):
                dict={'showMessage': True,'message': "You can not add any employee"}
                return render(request, 'showMessage.html', context=dict)
            

            user = userForm.save()
            user.set_password(user.password)
            user.save()

            userInfo = userInfoForm.save(commit=False)
            userInfo.user = user

            if 'proPic' in request.FILES:
                userInfo.proPic = request.FILES['proPic']

            userInfo.save()

            return HttpResponseRedirect(reverse('dashboard:seeAllEmployee'))
    
        else:
            userForm = userform(request.POST)
            userInfoForm = userformMoreinfo(request.POST)


    
    return render(request, 'authentication/registerUser.html', context=dict)





def loginApp(request):

    diction = {'username': '', 'password': ''}
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        diction.update({'username': username})
        diction.update({'password': password})

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard:dashboard'))
            else:
                diction.update({'message': "Account is not active"})

        else:
            diction.update({'message': "Password or username may be wrong"})

        
    return render(request, 'authentication/loginApp.html', context=diction)
                



@login_required
def logoutApp(request):
    logout(request)
    return HttpResponseRedirect(reverse('userAuth:index'))




@login_required
def employeeDelete(request, id):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)
    currentRole = currentUserMoreInfo.role

    if (currentRole != '1'):
        dict={'showMessage': True,'message': "Not found anything"}
        return render(request, 'showMessage.html', context=dict)
    
    user = User.objects.get(pk=id)
    userMoreInfo = models.userInfo.objects.get(user__pk=user.id)
    currentUserRole = userMoreInfo.role

    if currentUserRole == '1':
        userMoreInfo.role = "Chief"
    elif currentUserRole == '2':
        userMoreInfo.role = "Moderator"
    elif currentUserRole == '3':
        userMoreInfo.role = "Human Resource"
    elif currentUserRole == '4':
        userMoreInfo.role = "Accountant"
    else:
        userMoreInfo.role = "Office Employee"


    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        print(confirm)
        print(currentRole)
        if (confirm == "Delete") and (currentRole == '1'):
            user = User.objects.get(pk=id)
            userFname = user.first_name
            userLname = user.last_name
            message = userFname + " " + userLname + " is removed from your company"
            models.userInfo.objects.get(user__pk=user.id).delete()
            User.objects.get(pk=id).delete()

            dict={'showMessage': True,'message': message, 'showAddEmployees': True}
            return render(request, 'showMessage.html', context=dict)


    dict = {'user': user, 'userMoreInfo': userMoreInfo, 'showAddEmployees': True}

    dict.update({"employeeController": True})
    dict.update({"finaceController": True})
    dict.update({"fullEmployeeControler": True})

    return render(request, 'authentication/deleteUser.html', context=dict)
    
