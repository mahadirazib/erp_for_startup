from django.shortcuts import render

from userAuth.models import User, userInfo
from userAuth import models
from .models import notice

from .forms import addNotice, editNotice as editNotices
from userAuth.forms import userformMoreinfo, userform

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse



@login_required
def dashboardMainView(request):


    dict = {}

    if request.user.is_authenticated:

        currentUser = request.user

        dict.update({'myInfo' : currentUser})
        currentUserMoreInfo = userInfo.objects.get(user__pk = currentUser.id)
        dict.update({'myMoreInfo': currentUserMoreInfo})

        notices = notice.objects.filter(user=currentUserMoreInfo)
        dict.update({'notices': notices})


        if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "2"):

            notices = notice.objects.all()

            dict.update({'notices': notices})
            dict.update({"noticeController": True})


        if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "2" or currentUserMoreInfo.role == '3'):
            dict.update({"employeeController": True})
        
        
        if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "4"):
            dict.update({"finaceController": True})

        

    return render(request, 'dashboard/index.html', context=dict)





@login_required
def editProfile(request, id):

    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)
    currentRole = currentUserMoreInfo.role

    userForm = userform(instance=currentUser)
    userForm2 = userformMoreinfo(instance=currentUserMoreInfo)

    dict = {'userform': userForm, 'userform2': userForm2, 'alertMessage': "Login back after changing personal data."}

    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "2" or currentUserMoreInfo.role == "3" ):
        dict.update({"employeeController": True})

    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "4" ):
        dict.update({"finaceController": True})
    
    if (currentUserMoreInfo.role == "1"):
        dict.update({"fullEmployeeControler": True})

        

    if (currentRole == '1') or (currentRole == '3'):
        currentUser = User.objects.get(pk=id)
        currentUserMoreInfo = models.userInfo.objects.get(user__pk = currentUser.id)
        currentRole = currentUserMoreInfo.role
        userForm = userform(instance=currentUser)
        userForm2 = userformMoreinfo(instance=currentUserMoreInfo)
        dict.update({"changeRole": True})
        dict.update({'userform': userForm})
        dict.update({'userform2': userForm2})


    if request.method == 'POST':

        userForm = userform(request.POST, instance=currentUser)
        userForm2 = userformMoreinfo(request.POST, instance=currentUserMoreInfo)

        if userForm.is_valid() and userForm2.is_valid():

            changedrole = userForm2.cleaned_data['role']

            requestUser = request.user
            requestUserMoreInfo = models.userInfo.objects.get(user__pk = requestUser.id)
            requestUserRole = requestUserMoreInfo.role

            if (changedrole != currentRole) and (requestUserRole != '1'):
                dict={'showMessage': True,'message': "You can not change role"}
                return render(request, 'showMessage.html', context=dict)
            
            
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            userInfo = userForm2.save(commit=False)
            userInfo.user = user

            if 'proPic' in request.FILES:
                userInfo.proPic = request.FILES['proPic']

            userInfo.save()


            if user.id == requestUser.id:
                return HttpResponseRedirect(reverse('userAuth:loginApp'))
            
            
            dict={'showMessage': True,'message': "Successfully Updated" }
            return render(request, 'showMessage.html', context=dict)
        
        dict={'showMessage': True,'message': "Invalid Submission."}
        return render(request, 'showMessage.html', context=dict)


    return render(request, 'authentication/editUser.html', context=dict)





@login_required
def createNotice(request):

    dict = {'btnText': "Add Notice"}

    currentUser = request.user
    currentUserMoreInfo = userInfo.objects.get(user__pk = currentUser.id)

    if (currentUserMoreInfo.role == "1") or (currentUserMoreInfo.role == "2"):
        
        createNotice = addNotice
        dict.update({"createNotice": createNotice})

        dict.update({"employeeController": True})
        
        if (currentUserMoreInfo.role == "1"):
            dict.update({"finaceController": True})

        if request.method == "POST":

            noticeForm = addNotice(data=request.POST)

            if noticeForm.is_valid():
                noticeForm.save()
                dict.update({'message': "Notice added successfully"})
                return render(request, 'showMessage.html', context=dict)
            else:
                noticeForm = addNotice(request.POST)
                dict.update({"createNotice": noticeForm})

            return HttpResponseRedirect(reverse('dashboard:dashboard'))

        dict.update({'check': True})
        return render(request, 'notices/createNotice.html', context=dict)
    

    dict.update({'message': "You do not have the authority to make a notice"})
    return render(request, 'showMessage.html', context=dict)




@login_required
def editNotice(request, id):

    dict = {'btnText': "Edit Notice"}

    currentUser = request.user
    currentUserMoreInfo = userInfo.objects.get(user__pk = currentUser.id)


    if (currentUserMoreInfo.role == "1") or (currentUserMoreInfo.role == "2"):
        
        getNotice = notice.objects.get(pk=id)
        noticeForm = editNotices(instance=getNotice)
        dict.update({"createNotice": noticeForm})

        users = models.User.objects.all()
        dict.update({"users": users})

        dict.update({"employeeController": True})
        
        if (currentUserMoreInfo.role == "1"):
            dict.update({"finaceController": True})

        if request.method == "POST":

            noticeForm = editNotices(request.POST, instance=getNotice)

            if noticeForm.is_valid():
                noticeForm.save()
                dict.update({'message': "Notice Updated successfully"})
                return HttpResponseRedirect(reverse('dashboard:dashboard'))
                
            else:
                noticeForm = editNotices(request.POST)
                dict.update({"createNotice": noticeForm})


        dict.update({'check': True})
        return render(request, 'notices/createNotice.html', context=dict)
    

    dict.update({'message': "You do not have the authority to edit a notice"})
    return render(request, 'showMessage.html', context=dict)



@login_required
def deleteNotice(request, id):

    dict = {}

    currentUser = request.user
    currentUserMoreInfo = userInfo.objects.get(user__pk = currentUser.id)


    if (currentUserMoreInfo.role == "1") or (currentUserMoreInfo.role == "2"):
        
        notice.objects.get(pk=id).delete()
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    
    dict.update({'message': "You do not have the authority to delete a notice"})
    return render(request, 'showMessage.html', context=dict)



@login_required
def makeComplete(request, id):

    currentUser = request.user
    
    getNotice = notice.objects.get(pk=id)
    
    if getNotice.completedBy:
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    
    
    getNotice.completedBy = currentUser.id
    getNotice.save(update_fields=['completedBy'])

    return HttpResponseRedirect(reverse('dashboard:dashboard'))



@login_required
def makeIncomplete(request, id):

    getNotice = notice.objects.get(pk=id)
    
    
    getNotice.completedBy = ""
    getNotice.save(update_fields=['completedBy'])

    return HttpResponseRedirect(reverse('dashboard:dashboard'))







@login_required
def seeAllEmployee(request):

    dict = {}

    currentUser = request.user
    currentUserMoreInfo = userInfo.objects.get(user__pk = currentUser.id)

    if currentUser.is_authenticated:

        users = User.objects.all()
        usersMoreInfo = userInfo.objects.order_by('role').select_related("user")

        dict.update({'users' : users})
        dict.update({'userMoreInfo': usersMoreInfo})

        if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "2" or currentUserMoreInfo.role == "3" ):
            dict.update({"employeeController": True})

        if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "4" ):
            dict.update({"finaceController": True})
        
        if (currentUserMoreInfo.role == "1"):
            dict.update({"fullEmployeeControler": True})

        return render(request, 'seeAllEmployee/allUserDetails.html', context=dict)
    
    dict.update({'message': "You does not have authority to see the employee"})
    return render(request, 'showMessage.html', context=dict)


