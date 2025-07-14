
from django.urls import path,include
from . import views



urlpatterns = [
     path("login/", views.Login,name='login'),
     path("register/", views.Register,name='register'),
     path("addSeller/", views.AddSeller, name='addSeller'),
     path("addBroker/", views.AddBroker, name='addBroker'),
     path("addApartment/", views.AddApartment, name='addApartment'),
     path("addImage/<int:id>", views.AddImage, name='addImage'),
     path('addInquiries/<int:id>/', views.addInquries, name='addInquiries'),
     path("apartment/", views.ApartmentList, name='apartment'),
     path("inquiries/", views.InquiriesList, name='inquiries'),
     path("buy/:<int:id>", views.buy, name='buy'),

     # path("app1/", include('App1.urls'))

]
