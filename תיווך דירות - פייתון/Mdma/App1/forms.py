from django import forms
from .models import Image,Inquiries,Apartment,Seller,Broker

#class SellerModelForm (forms.ModelForm):


class InquiriesModelForm(forms.ModelForm):
    class Meta:
        model = Inquiries
        fields = ['date']

class ImageModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class ApartmentModelForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['state','describe', 'price','rooms','floor','street','neighborhood','city','brokerage','status']

class SellerModelForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = []

class BrokerModelForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = []


