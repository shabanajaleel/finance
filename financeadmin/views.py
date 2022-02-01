from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import partnerform, partnershipform, projectform,profitform
from . models import partner, partnership, project,profit,Partnerpayment
from django.core.paginator import Paginator
from django.db.models import Sum,Count
from django.db.models import Q

# Create your views here.
def fnlogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(fnhome)
        else:
            messages.error(request,"invalid username or password")
    return render(request,'login.html')

@login_required(login_url="/login/")
def fnhome(request):
    return render(request,'home.html')

def fnlogout(request):
    logout(request)
    return redirect(fnlogin)

@login_required(login_url="/login/")
def fnaddproject(request):
    form=projectform()
    context={"form" : form}
    if request.method=="POST":
        form=projectform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Project added successfilly")
            return render(request,'addproject.html',context)
        else:
            messages.error(request,"OOps,something went wrong")

    
    return render(request,'addproject.html',context)


@login_required(login_url="/login/")
def fnviewproject(request):
    projects=project.objects.all()
    sum_dict={}
    sum_list=[]
    for i in projects:
        sum1=partnership.objects.filter(project=i.id).aggregate(mysum=Sum('partnership'))['mysum'] or 0.00
        sum_dict['name']=i.name
        sum_dict['sum']=sum1
        sum_list.append(sum_dict.copy())
        sum_dict={}
    paginator=Paginator(projects,3)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)
    context={'page':page_obj,'sum_list':sum_list}
    return render(request,"viewproject.html",context)

# Add Profit

@login_required(login_url="/login/")
def fnaddprofit(request):
    form=profitform
    if request.method=="POST":
        form=profitform(request.POST)
        if form.is_valid():
            p=form.save()
            payment_id=p.id
            print(payment_id)
            project_id=p.project_id
            print(project_id)
            partners=partnership.objects.filter(project=project_id)
            for i in partners:
                percent=i.partnership
                newamount=(percent * p.amount)/100
                payment=Partnerpayment(payment_id=payment_id,partner=i.partner,amount=newamount,created_date=p.created_date).save()
            messages.success(request,'profit added successfully')
            return redirect(fnaddprofit)
        else:
            messages.error(request,'invalid entries')
            return redirect(fnaddprofit)

    context={'form':form}
    return render(request,'addprofit.html',context)

# view Profit

@login_required(login_url="/login/")
def fnviewprofit(request):
    profits=profit.objects.filter(amount__gt=0)
    context={'profits':profits}
    return render(request,'viewprofit.html',context)

# Delete Profit

def fndeleteprofit(request,prof_id):
    profits=profit.objects.get(id=prof_id)
    profits.amount -= profits.amount
    profits.save()
    payment_id=profits.id
    project_id=profits.project_id
    partners=partnership.objects.filter(project=project_id)
    for i in partners:
        percent=i.partnership
        newamount=(percent * profits.amount)/100
        print(newamount)
        payment=Partnerpayment.objects.filter(payment_id=payment_id)
        for k in payment:
            k.amount=newamount
            k.save()
    messages.success(request,'profit deleted successfully')
    return redirect(fnviewprofit)
    






@login_required(login_url="/login/")
def fnviewpartner(request):
    q=request.GET.get('q') if request.GET.get('q') !=None  else ''
    t=request.GET.get('t') if request.GET.get('t') !=None  else ''
    print(q)
    partners=partner.objects.all()
    if q:
        partners=partners.filter(partner_name__icontains=q)
    if t:
        partners=partners.filter(partnership__project__name=t)
    context={'partner':partners}
    return render(request,'viewpartners.html',context)

@login_required(login_url="/login/")
def fnaddpartner(request):
    project_model=project.objects.all()
    form1=partnerform()
    form2=partnershipform()
    context={'form1':form1,'form2':form2,'project_model':project_model}
    if request.method=="POST":
        form1=partnerform(request.POST)
        partnername=request.POST.get('partner_name')
        check_list=request.POST.getlist('check')
        newcheck_list=[i for i in check_list if i]
        print(newcheck_list)
        partnership_list=request.POST.getlist('partnership')
        newpartneship_list=[j for j in partnership_list if j]
        print(newpartneship_list)
        p=partner.objects.filter(partner_name=partnername).exists()
        if p == False:
            if form1.is_valid():
                p1=form1.save()
                print(len(newcheck_list))
                for z in range(0,len(newcheck_list)):
                    print(z)
                    print(newcheck_list[z])
                    print(newpartneship_list[z])
                    sum1=partnership.objects.filter(project=newcheck_list[z]).aggregate(mysum=Sum('partnership'))['mysum'] or 0.00
                    sum2=100-sum1
                    if int(newpartneship_list[z]) <= sum2: 
                        newpart=partnership(project_id=newcheck_list[z],partner_id=p1.id,partnership=newpartneship_list[z])
                        newpart.save()
                    else:messages.error(request,'partnership exceeds 100')
                messages.success(request,'partners added successfully')
                return redirect(fnaddpartner)
                       
        else:
            messages.success(request,'partners already exist')
            return redirect(fnaddpartner)                    
    return render(request,'addpartnernew.html',context)

@login_required(login_url="/login/")                            
def fnstatement(request):
    if request.method=="POST":
        from_date=request.POST['from']
        to_date=request.POST['to']
        opening=Partnerpayment.objects.filter(created_date__lt=from_date)
        partners=partner.objects.filter()
        opening_list=[]
        opening_dict={}
        for q in partners:
            profit=opening.filter(partner_id=q.id).aggregate(Sum('amount'))
            opening_dict['partner']=q.partner_name
            opening_dict['amount']=profit['amount__sum']
            opening_list.append(opening_dict.copy())
        print(opening_list)

        profit_interval=Partnerpayment.objects.filter(created_date__gte=from_date,created_date__lte=to_date)
        partner_list=[]
        partner_dict={}
        sum=0
        for p in partners:
            profit=profit_interval.filter(partner_id=p.id).aggregate(Sum('amount'))
            partner_dict['partner']=p.partner_name
            partner_dict['amount']=profit['amount__sum']
            partner_list.append(partner_dict.copy())
            sum += profit['amount__sum']
        print(partner_list)
        return render(request,'statements.html',{'data':partner_list,'opening':opening_list,'total':sum})

    return render(request,'statements.html')



                


       
       
       
   
                            
                   

    



