from django.urls import path
from . import views

urlpatterns=[
    path('login',views.fnlogin,name="login"),
    path('logout',views.fnlogout,name="logout"),

    path('home/',views.fnhome,name="home"),
    path('addproject/', views.fnaddproject,name="addproject"),
    path('viewproject/', views.fnviewproject,name="viewproject"),

    path('addpartner/', views.fnaddpartner,name="addpartner"),

    path('addprofit/', views.fnaddprofit,name="addprofit"),

]