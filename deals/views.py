from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from userAuth import models
from .models import currentDeals, allDealsRecord

from . import forms

# Create your views here.


@login_required
def dealsMainView(request):
    
    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk=currentUser.id)

    dict = {}

    if currentUserMoreInfo.role == "1":
        dict.update({"fullEmployeeControler": True})
        dict.update({"employeeController": True})
        dict.update({"finaceController": True})
        dict.update({"dealController": True})

        allCurrentDeals = currentDeals.objects.all()

        dict.update({'allDeals': allCurrentDeals})
        


    if currentUserMoreInfo.role == "2":
        dict.update({"employeeController": True})

        allCurrentDeals = currentDeals.objects.filter(whoCanSee=currentUserMoreInfo)

        dict.update({'allDeals': allCurrentDeals})



    if currentUserMoreInfo.role == '3':
        dict.update({"employeeController": True})
        
        allCurrentDeals = currentDeals.objects.filter(whoCanSee=currentUserMoreInfo)

        dict.update({'allDeals': allCurrentDeals})



    if currentUserMoreInfo.role == "4":
        dict.update({"finaceController": True})

        allCurrentDeals = currentDeals.objects.filter(whoCanSee=currentUserMoreInfo)

        dict.update({'allDeals': allCurrentDeals})

    if currentUserMoreInfo.role == "5":
        dict.update({'noControl': True})

        allCurrentDeals = currentDeals.objects.filter(whoCanSee=currentUserMoreInfo)

        dict.update({'allDeals': allCurrentDeals})


    return render(request, 'deals/dealsMain.html', context=dict)



@login_required
def registerNewDeal(request):
    
    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk=currentUser.id)
    
    dict = {}

    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "4"):
        dict.update({"finaceController": True})


    if currentUserMoreInfo.role == "1":
        dict.update({'check': True})

        dealRegisterForm = forms.registerNewDeals
        dict.update({'dealRegisterForm':dealRegisterForm})
        dict.update({'btnText': 'Submit'})

        if request.method == 'POST':
            dealRegisterForm = forms.registerNewDeals(data=request.POST)
            
            if dealRegisterForm.is_valid():
                dealRegisterForm.save()
                return HttpResponseRedirect(reverse('deals:deals'))

            else:
                dict.update({'dealRegisterForm':dealRegisterForm})
                dict.update({'message': 'Something went wrong'})

        return render(request, 'deals/addEditDeals.html', context=dict)
    
    
    dict.update({'message': "You are on the wrong page"})
    return render(request, 'showMessage.html', context=dict)



@login_required
def editDeal(request, id):
    
    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk=currentUser.id)
    
    dict = {}

    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "4"):
        dict.update({"finaceController": True})


    if currentUserMoreInfo.role == "1":
        dict.update({'check': True})
        dict.update({'dealController': True})

        deal = currentDeals.objects.get(pk=id)
        dealRegisterForm = forms.registerNewDeals(instance=deal)
        dict.update({'dealRegisterForm':dealRegisterForm})
        dict.update({'btnText': 'Update'})

        if request.method == 'POST':
            dealRegisterForm = forms.registerNewDeals(data=request.POST, instance=deal)
            
            if dealRegisterForm.is_valid():
                dealRegisterForm.save()
                return HttpResponseRedirect(reverse('deals:deals'))

            else:
                dict.update({'dealRegisterForm':dealRegisterForm})
                dict.update({'message': 'Something went wrong'})

        return render(request, 'deals/addEditDeals.html', context=dict)
    
    
    dict.update({'message': "You are on the wrong page"})
    return render(request, 'showMessage.html', context=dict)







@login_required
def terminateOrEndDeals(request, id, endOrTerminate):
    
    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk=currentUser.id)
    
    dict = {}

    if (currentUserMoreInfo.role == "1" or currentUserMoreInfo.role == "4"):
        dict.update({"finaceController": True})


    if currentUserMoreInfo.role == "1":
        dict.update({'check': True})
        dict.update({'dealController': True})

        deal = currentDeals.objects.get(pk=id)

        endCurrentDeal = allDealsRecord(dealWith=deal.dealWith)
        endCurrentDeal.giveOrReceive = deal.giveOrReceive
        endCurrentDeal.dealAmount = deal.dealAmount
        endCurrentDeal.dealTitle = deal.dealTitle
        endCurrentDeal.dealDescription = deal.dealDescription
        endCurrentDeal.dealEnds = deal.dealEnds
        endCurrentDeal.completeOrTerminated = endOrTerminate
        endCurrentDeal.save()

        deal.delete()

        return HttpResponseRedirect(reverse('deals:deals'))
    
    
    dict.update({'message': "You are on the wrong page"})
    return render(request, 'showMessage.html', context=dict)







@login_required
def oldDeals(request):
    
    currentUser = request.user
    currentUserMoreInfo = models.userInfo.objects.get(user__pk=currentUser.id)

    dict = {}

    if currentUserMoreInfo.role == "1":
        dict.update({"employeeController": True})
        dict.update({"finaceController": True})
        dict.update({"dealController": True})
        dict.update({"oldDeals": True})

        allOldDeals = allDealsRecord.objects.all()

        dict.update({'allDeals': allOldDeals})



    return render(request, 'deals/dealsMain.html', context=dict)


