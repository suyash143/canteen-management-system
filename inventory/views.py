from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from . import models
from django.contrib import messages
from django.core.paginator import Paginator


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,"invalid Credentials")
            return redirect('login')
    else:
        return render(request,'login.html')


def dashboard(request):
    return render(request,'dashboard.html')


def inventory(request):
    name = models.Supplies.objects.all()
    name_paginator = Paginator(name, 130)
    page_num = request.GET.get('page')
    page = name_paginator.get_page(page_num)
    return render(request,'inventory.html',{'page':page})


def inventory_add(request):
    return render(request,'dashboard.html')


def logout(request):
    auth.logout(request)
    latest = User.objects.latest('pk')

    id=latest.pk

    return redirect('login')


def dashboard_inventory(request):
    script=models.Supplies.objects.all()

    if request.method=="POST" and 'id' in request.POST:
        id=request.POST['id']
        request.session['id']=id
        return redirect('dashboard_inventory_edit')

    return render(request,'dashboard_inventory.html',{'script':script})


def dashboard_inventory_edit(request):
    id=request.session['id']
    print(id)
    if id:
        script=models.Supplies.objects.all().get(pk=id)
        if request.method=='POST':

            name = request.POST['name']
            stock = request.POST['stock']
            minimum=request.POST['minimum']

            script.name=name
            script.stock=stock
            script.minimum=minimum
            script.save()
        return render(request, "dashboard_inventory_edit.html", {'script': script})

    return render(request,"dashboard_inventory_edit.html")


def dashboard_inventory_delete(request):
    script_id = request.session['id']
    obj=models.Supplies.objects.get(pk=script_id)
    obj.delete()
    return redirect('dashboard_inventory')


def dashboard_inventory_add(request):

    if request.method == 'POST':
        name = request.POST['name']
        platform = request.POST['platform']

        sc, created = models.LeadSource.objects.get_or_create(name=name,platform=platform,is_active=1)
        sc.save()

    return render(request,"dashboard_inventory_edit.html")