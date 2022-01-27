from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import partnerform, partnershipform, projectform,profitform
from . models import partner, partnership, project,profit
from django.core.paginator import Paginator
from django.db.models import Sum
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




def fnaddpartner1(request):
    project_model=project.objects.all()
    form1=partnerform()
    form2=partnershipform()
    context={'form1':form1,'form2':form2,'project_model':project_model}
    if request.method=="POST":
        form1=partnerform(request.POST)
        partnername=request.POST.get('partner_name')
        projectid=request.POST.get('project')
        partnership1=int(request.POST.get('partnership'))

        if form1.is_valid():
            part_obj=partner.objects.filter(partner_name=partnername).exists()
            print(part_obj)
            if part_obj==True:
                p=partner.objects.get(partner_name=partnername)
                if form2.is_valid():                              
                    proj_obj=partnership.objects.filter(project=projectid,partner=p.id).exists()
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

    return render(request,'addpartnernew.html',context)

def fnaddprofit(request):
    form=profitform
    if request.method=="POST":
        form=profitform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'profit added successfully')
            return redirect(fnaddprofit)
        else:
            messages.error(request,'invalid entries')
            return redirect(fnaddprofit)

    context={'form':form}
    return render(request,'addprofit.html',context)

def fnviewprofit(request):
    profits=profit.objects.all()
    context={'profits':profits}
    return render(request,'viewprofit.html',context)

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
        if form1.is_valid():
            p=form1.save()
            
            for z in range(0,len(newcheck_list)):
                print(z)
                print(newcheck_list[z])
                print(newpartneship_list[z])
                sum1=partnership.objects.filter(project=newcheck_list[z]).aggregate(mysum=Sum('partnership'))['mysum'] or 0.00
                sum2=100-sum1
                if int(newpartneship_list[z]) <= sum2: 
                    newpart=partnership(project_id=newcheck_list[z],partner_id=p.id,partnership=newpartneship_list[z])
                    newpart.save()
                    messages.success(request,'partners added successfully')
                    return redirect(fnaddpartner)
                else:
                    messages.error(request,'partnership exceeds 100')                    
    return render(request,'addpartnernew.html',context)

                            
                        
            
            # if part_obj==True:
            #     p=partner.objects.get(partner_name=partnername) 
            #     for i in check_list:
            #         if i != '':
            #             proj_obj=partnership.objects.filter(project=i,partner=p.id).exists()
            #             if proj_obj==False:
            #                 sum1=partnership.objects.filter(project=i).aggregate(mysum=Sum('partnership'))['mysum'] or 0.00
            #                 sum2=100-sum1
            #                 for j in partnership_list:
            #                     if int(j) <= sum2:
            #                         newpart=partnership(project_id=i,partner_id=p.id,partnership=j)
            #                         newpart.save()
            #                         messages.success(request,'partners added successfully')
            #                         return redirect(fnaddpartner)
            #                     else:
            #                         messages.error(request,'Partnership exceeds 100')
            #                         return redirect(fnaddpartner)

            #                 else:
            #                     messages.error(request,'partner with selected project exists')
            #                     return redirect(fnaddpartner)
            #             else:
                            
                            
                   

    



