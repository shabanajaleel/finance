from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.fnlogin,name="login"),
    path('logout/',views.fnlogout,name="logout"),

    path('home/',views.fnhome,name="home"),
    path('addproject/', views.fnaddproject,name="addproject"),
    path('viewproject/', views.fnviewproject,name="viewproject"),

    path('addpartner/', views.fnaddpartner,name="addpartner"),
    path('viewpartner/', views.fnviewpartner,name="viewpartner"),

    path('addprofit/', views.fnaddprofit,name="addprofit"),
    path('viewprofit/', views.fnviewprofit,name="viewprofit"),
    path('profitdelete/<prof_id>', views.fndeleteprofit,name="profitdelete"),


    path('statements/',views.fnstatement,name="statements")

]