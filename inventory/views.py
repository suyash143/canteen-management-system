from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from . import models
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from string import digits, ascii_letters
import random
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template


def index(request):
    return render(request,'index.html')


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
    user=request.user
    items=models.Order.objects.filter(ordered_by=user)
    total_orders=0
    total_amount=0
    total_credit=0
    for item in items:
        total_orders+=1
        total_amount+=item.amount
        if item.transaction_mode=='Credit':
            total_credit+=item.amount
    
    context={'total_orders':total_orders,'total_amount':total_amount,'total_credit':total_credit}
    return render(request,'dashboard.html',context)


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
        stock = request.POST['stock']
        minimum = request.POST['minimum']

        sc, created = models.Supplies.objects.get_or_create(name=name,stock=stock,minimum=minimum)
        sc.save()

    return render(request,"dashboard_inventory_edit.html")


def dashboard_create_order(request):
    first_name=request.session.get('first_name','')
    last_name = request.session.get('last_name', '')
    email = request.session.get('email', '')
    items = request.session.get('items', '')
    amount = request.session.get('amount', '')
    mode_of_transaction = request.session.get('mode_of_transaction', '')
    defaults = {'first_name':first_name,'last_name':last_name,'email':email,'items':items,
                'amount':amount,'mode_of_transaction':mode_of_transaction}

    if request.method=='POST' and 'otp' in request.POST:
        first_name=request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email=request.POST.get('email')
        items = request.POST.get('items')
        amount = request.POST.get('amount')
        mode_of_transaction = request.POST.get('mode_of_transaction')
        name=first_name+last_name
        request.session['first_name']=first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        request.session['items'] = items
        request.session['amount'] = amount
        request.session['mode_of_transaction'] = mode_of_transaction
        try:
            user=models.User.objects.get(email=email)
            otp=''
            for i in range(6):
                otp += random.choice(digits)
            user.info.otp=otp
            user.save()
            data=user

            subject = 'Welcome to Union Canteen'
            trainer = 0
            updater = data

            html_message = render_to_string('otp.html',
                                            {'otp': otp,'active':False
                                             })
            plain_message = strip_tags(html_message)
            from_email = 'suyash@we-fit.in'
            to = updater.email

            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            return redirect('dashboard_create_order')


        except:
            s=''
            for i in range(3):
                s += random.choice(digits)
            username=first_name.strip()+last_name.strip()+s.strip()

            password = ''
            for i in range(12):
                password += random.choice(digits+ascii_letters)

            otp = ''
            for i in range(6):
                otp += random.choice(digits)

            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.save()
            user.info.otp=otp
            user.save()

            data = user

            subject = 'Welcome to Union Canteen'
            trainer = 0
            updater = data

            html_message = render_to_string('otp.html',
                                            {'otp': otp,'active':True,'username':username, 'password':password,
                                             })
            plain_message = strip_tags(html_message)
            from_email = 'suyash@we-fit.in'
            to = updater.email

            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            '''sc, created = models.Order.objects.get_or_create(name=name, ordered_by=user, items=items,
                                                             created=datetime.datetime.now(), taken_by=request.user,
                                                             amount=amount,transaction_mode=mode_of_transaction)
            sc.save()'''
            return redirect('dashboard_create_order')

    elif request.method == 'POST' and 'submit' in request.POST:
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        items = request.POST.get('items')
        amount = request.POST.get('amount')
        mode_of_transaction = request.POST.get('mode_of_transaction')
        first_name = request.session.get('first_name', '')
        last_name = request.session.get('last_name', '')

        name = first_name + last_name

        user = models.User.objects.get(email=email)
        print(user.info.otp)
        if request.POST.get('otp_value')==user.info.otp:
            sc, created = models.Order.objects.get_or_create(ordered_by=user, items=items,
                                                             created=datetime.datetime.now(), taken_by=request.user,
                                                             amount=amount, transaction_mode=mode_of_transaction)
            sc.save()

            data = sc

            subject = f'Invoice for order:{sc.transaction_id}'
            trainer = 0
            updater = data

            html_message = render_to_string('invoice.html',
                                            {'data': data,
                                             })
            plain_message = strip_tags(html_message)
            from_email = 'suyash@we-fit.in'
            to = user.email

            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


            request.session['first_name'] = ''
            request.session['last_name'] = ''
            request.session['email'] = ''
            request.session['items'] = ''
            request.session['amount'] = ''
            request.session['mode_of_transaction'] = ''
            return redirect('dashboard')

    return render(request,'dashboard_create_order.html',{'defaults':defaults})


def inventory_search(request):
    if request.method == 'GET':  # this will be GET now
        query = request.GET.get('search')
        print(query)

        script =  models.Supplies.objects.filter(name__icontains=query)

        return render(request,'dashboard_inventory.html',{'script':script})

    else:

        if request.method == "POST" and 'id' in request.POST:
            id = request.POST['id']
            request.session['id'] = id
            return redirect('dashboard_inventory_edit')


def pdf_download(request):
    template_path = 'pdf_view.html'

    context = {'data': 'data'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

