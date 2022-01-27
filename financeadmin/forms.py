from sqlite3 import Date
from django import forms
from . models import profit, project,partner,partnership

class DateInput(forms.DateInput):
    input_type = 'date'


class projectform(forms.ModelForm):
    class Meta:
        model=project
        fields="__all__"
        labels={
            'name':"Project Name"
        }
        widgets={
           'name': forms.TextInput(attrs={'class':"form-control"})
        }

class partnerform(forms.ModelForm):
    class Meta:
        model=partner
        fields="__all__"
        labels={
            'partner_name':"Partner Name"
        }
        widgets={
           'partner_name': forms.TextInput(attrs={'class':"form-control"})
        }

class partnershipform(forms.ModelForm):
    class Meta:
        model=partnership
        fields="__all__"
        exclude=['partner']
        labels={
            'project':'Project Name',
            'partnership':'Partnership (in %)'
        }
        widgets={
           'project':forms.Select(attrs={'class':"form-control"}),
           'partnership':forms.NumberInput(attrs={'class':"form-control"})
        }

class profitform(forms.ModelForm):
   
    class Meta:
        model=profit
        fields="__all__"
        labels={
            'created_date':'Date',
            'project':'Project Name',
            'amount':'Profit Amount(in Rs)'
        }
        widgets={
            'created_date':DateInput(attrs={'class':"form-control"}),
            'project':forms.Select(attrs={'class':"form-control"}),
            'amount':forms.NumberInput(attrs={'class':"form-control"})
        }
        # def __init__(self,*args,**kargs):
        #     super(profitform,self).__init__(*args,**kargs)
        #     for name in self.fields.keys():
        #         self.fields[name].widget.attrs.update({'class':'form-control'})

        