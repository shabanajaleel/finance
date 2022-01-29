from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import partnerform, partnershipform, projectform,profitform
from . models import partner, partnership, project,profit
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

def fnhome(request):
    return render(request,'home.html')

def fnlogout(request):
    logout(request)
    return redirect(fnlogin)

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
                messages.success(request,'partners added successfully')
                return redirect(fnaddpartner)
                       
        else:
            messages.success(request,'partners already exist')
            return redirect(fnaddpartner)                    
    return render(request,'addpartnernew.html',context)

                            
def fnstatement(request):
    if request.method=="POST":
        from_date=request.POST['from']
        to_date=request.POST['to']
        print(from_date)
        print(to_date)
        profit_interval=profit.objects.filter(created_date__gte=from_date,created_date__lte=to_date)
        print(profit_interval)
        profit_dict={}
        profit_list=[]
        for q in profit_interval:
            newinterval=profit_interval.filter(project=q.project).aggregate(Sum('amount'))
            profit_dict['project']=q.project.id
            profit_dict['value']=newinterval['amount__sum']
            profit_list.append(profit_dict.copy())
        new_list=[i for n, i in enumerate(profit_list) if i not in profit_list[n + 1:]]
        print(new_list)
        partners=partner.objects.all()
        partner_list=[]
        for partner1 in partners:
            projects=partner1.partnership_set.all()
            project_list=[]
            for p in projects:
                project_dic={}
                for m in new_list:
                    if m['project'] == p.project_id:
                        percent=p.partnership
                        some=m['value']
                        calculate=(percent*some)/100
                        project_dic['partner']=p.partner
                        project_dic['project']=p.project
                        project_dic['amount']=calculate
                project_list.append(project_dic.copy())
            partner_list.extend(project_list)
            new_partner_list=[i for i in partner_list if i]

        print(new_partner_list)
        return render(request,'statements.html',{'data':new_partner_list})


                    


                
                        # print(p.project)
            # for profits in profit_interval:
            #     if projects.project == profits.project:
            #         newinterval=profits.filter(project=profits.project).aggregate(Sum('amount'))
            #         print(newinterval)




        # profit_dict={}
        # profit_list=[]
        # for q in profit_interval:
        #     newinterval=profit_interval.filter(project=q.project).aggregate(Sum('amount'))
        #     profit_dict['project']=q.project.id
        #     profit_dict['value']=newinterval['amount__sum']
        #     profit_list.append(profit_dict.copy())
        # new_list=[i for n, i in enumerate(profit_list) if i not in profit_list[n + 1:]]
        # print(new_list)
        # for m in new_list:
        #     # print(m)
        #     sum_amount=[]
        #     sum_dict={}
        #     partnership_list=partnership.objects.filter(project=m['project'])
        #     for h in partnership_list:
        #         print(h.partnership)
        #         percent=h.partnership
        #         some=m['value']
        #         calculate=(percent*some)/100
        #         sum_dict['project']=h.project
        #         sum_dict['partner']=h.partner
        #         sum_dict['amount']=calculate
        #         sum_amount.append(sum_dict.copy())
        #     print(sum_amount)
            
        #     context={'amount':sum_amount}
        # return render(request,'statements.html',context)
    return render(request,'statements.html')






            # partners=partner.objects.all()
            # for i in partners:
            #     partnership_list=i.partnership_set.all()
            #     for j in partnership_list:
            #         print(j.project)
            #         if j.project == q.project:
            #             part=partnership.objects.filter(project=j.project,partner=i.id)
                       

            
        # projects=project.objects.all()
        # for p in projects:
        #     newinterval=profit_interval.filter(project=p.id).aggregate(Sum('amount'))
        #     # print(newinterval)
        #     partnership_table=partnership.objects.filter(project=p.id)
        #     for i in partnership_table:
        #         print(i.partner)
                


       
       
       
   
                            
                   

    



