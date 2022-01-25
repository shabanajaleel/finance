from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import partnerform, partnershipform, projectform,profitform
from . models import partner, partnership, project,profit
from django.core.paginator import Paginator
from django.db.models import Sum

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

def fnhome(request):
    return render(request,'home.html')

def fnlogout(request):
    logout(request)
    return redirect(fnlogin)

def fnaddproject(request):
    if request.method=="POST":
        form=projectform(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request,"OOps,something went wrong")

    form=projectform()
    context={"form" : form}
    return render(request,'addproject.html',context)

def fnviewproject(request):
    projects=project.objects.all()
    # for i in projects:
    #     sum1=partnership.objects.filter(project=i.id).aggregate(mysum=Sum('partnership'))['mysum'] or 0.00
    print(projects)
    paginator=Paginator(projects,3)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)
    context={'page':page_obj}
    return render(request,"viewproject.html",context)

def fnaddpartner(request):
    form1=partnerform()
    form2=partnershipform()
    context={'form1':form1,'form2':form2}
    if request.method=="POST":
        form1=partnerform(request.POST)
        partnername=request.POST.get('partner_name')
        form2=partnershipform(request.POST)
        projectid=request.POST.get('project')
        partnership1=int(request.POST.get('partnership'))

        if form1.is_valid():
            part_obj=partner.objects.filter(partner_name=partnername).exists()
            print(part_obj)
            if part_obj==True:
                p=partner.objects.get(partner_name=partnername)
                if form2.is_valid():                              
                    proj_obj=partnership.objects.filter(project=projectid).exists()
                    if proj_obj==False:
                        sum1=partnership.objects.filter(project=projectid).aggregate(mysum=Sum('partnership'))['mysum'] or 0.00
                        sum2=100-sum1
                        if partnership1 <= sum2:
                            newpart=form2.save(commit=False)
                            newpart.partner_id=p.id
                            newpart.save()
                            messages.success(request,'partners added successfully')
                            return redirect(fnaddpartner)
                        else:
                            messages.error(request,'Partnership exceeds 100')
                            return redirect(fnaddpartner)

                    else:
                        messages.error(request,'partner with selected project exists')
                        return redirect(fnaddpartner)
            else:
                sum1=partnership.objects.filter(project=projectid).aggregate(mysum=Sum('partnership'))['mysum'] or 0.00
                
                sum2=100-sum1
                if partnership1 <= sum2:
                    p=form1.save()
                    if form2.is_valid():
                        newpart=form2.save(commit=False)
                        newpart.partner_id=p.id
                        newpart.save()
                        messages.success(request,'partners added successfully')
                        return redirect(fnaddpartner)
                else:
                    messages.error(request,'Partnership exceeds 100')
                    return redirect(fnaddpartner)

    return render(request,'addpartner.html',context)

def fnaddprofit(request):
    form=profitform
    context={'form':form}
    return render(request,'addprofit.html',context)


