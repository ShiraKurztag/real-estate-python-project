from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SellerModelForm,BrokerModelForm,ApartmentModelForm,ImageModelForm,InquiriesModelForm
from django.db import transaction
from .models import Apartment,Image,Inquiries,Broker,Seller,User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# ROLE=False
# ID=0
def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        user_type = request.POST.get('user_type', None)
        if not user_type:
            return render(request, 'Register.html', {'form': form, 'error': 'User type is required'})
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                # עדכון שדה first_name לפי סוג המשתמש
                if user_type == 'seller':
                    user.first_name = 'seller'
                    # הוספת המשתמש כמוכר
                    with transaction.atomic():
                        seller = Seller(user=user)
                        seller.save()
                elif user_type == 'broker':
                    user.first_name = 'broker'
                    # הוספת המשתמש כמתווך
                    with transaction.atomic():
                        broker = Broker(user=user, benefits=0)  # ניתן להוסיף ערכים נוספים כאן
                        broker.save()
                else:
                    user.first_name = 'user'
                user.save()  # שמירה אחרי העדכון
                return redirect('/app1/login')
    else:
        form = UserCreationForm()
    return render(request, 'Register.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            with transaction.atomic():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        seller=Seller.objects.all()
                        broker=Broker.objects.all()
                    return redirect('/')
    form = AuthenticationForm()
    return render(request, 'Login.html', {'form': form})

def AddSeller(request):
    if request.method == 'POST':
        # formUser = UserCreationForm(request.POST)
        sellerForm = SellerModelForm(request.POST, request.FILES)
        if sellerForm.is_valid():
            with transaction.atomic():
                seller = sellerForm.save(commit=False)
                seller.user = request.user
                seller.save()
                return redirect('/app1/apartment')
    formSeller = SellerModelForm()
    return render(request, 'AddSeller.html', {'formSeller':formSeller})

def AddBroker(request):
    if request.method == 'POST':
        # formUser = UserCreationForm(request.POST)
        brokerForm = BrokerModelForm(request.POST, request.FILES)
        if brokerForm.is_valid():
            with transaction.atomic():
                broker = brokerForm.save(commit=False)
                broker.user = request.user
                broker.benefits=0
                broker.save()
                return redirect('/app1/apartment')
    formBroker= BrokerModelForm()
    return render(request, 'AddBroker.html', {'formBroker':formBroker})
@login_required
def AddApartment(request):
    if request.method == 'POST':
        apartmentForm = ApartmentModelForm(request.POST, request.FILES)
        imageForm = ImageModelForm(request.POST, request.FILES)

        if apartmentForm.is_valid():
            with transaction.atomic():
                # שמירת פרטי הדירה
                apartment = apartmentForm.save(commit=False)
                apartment.seller = request.user  # הקצאת המשתמש
                apartment.save()

                # שמירת התמונות אם קיימות
                if 'image' in request.FILES:
                    images = request.FILES.getlist('image')
                    for img in images:
                        image = Image(image=img, apartment=apartment)
                        image.save()

                return redirect('/app1/apartment')
    else:
        apartmentForm = ApartmentModelForm()
        imageForm = ImageModelForm()

    return render(request, 'AddApartment.html', {'formApartment': apartmentForm, 'formImage': imageForm})

@login_required
def AddImage(request,id):
    if request.method == 'POST':
        # formUser = UserCreationForm(request.POST)
        imageForm = ImageModelForm(request.POST, request.FILES)
        if imageForm.is_valid():
            with transaction.atomic():
                image = imageForm.cleaned_data['image']
                img = imageForm.save(commit=False)
                img.image=image
                apartment=Apartment.objects.get(id=id)
                img.apartment=apartment
                img.save()
                return redirect('/app1/apartment')
    imageForm= ImageModelForm()
    return render(request, 'AddImage.html', {'formImage':imageForm})


from django.shortcuts import get_object_or_404


@login_required
def addInquries(request, id):
    if request.method == 'POST':
        inquiriesForm = InquiriesModelForm(request.POST, request.FILES)
        if inquiriesForm.is_valid():
            with transaction.atomic():
                user = request.user
                inquiries = inquiriesForm.save(commit=False)
                inquiries.user = user
                apartment = get_object_or_404(Apartment, id=id)
                inquiries.apartment = apartment
                inquiries.save()
                return redirect('/app1/apartment')
    else:
        inquiriesForm = InquiriesModelForm()
    return render(request, 'AddInquiries.html', {'formInquiries': inquiriesForm})

@login_required
def ApartmentList(request):
    if request.method == "POST":
        value = request.POST.get('svalue')
        select = request.POST.get('stype')
        if select == 'price':
            apartmentList = Apartment.objects.filter(price__icontains=value, status=False)
        elif select == 'seller':
            apartmentList = Apartment.objects.filter(seller__icontains=value, status=False)
        else:
            apartmentList = Apartment.objects.filter(city__icontains=value, status=False)
    else:
          apartmentList = Apartment.objects.filter(status=False)
    role = request.user.first_name
    imageList=Image.objects.all()
    data = {
        'apartments': apartmentList,
        'images':imageList,
        'role': role
    }
    return render(request,'ApartmentList.html', data)
@login_required
def InquiriesList(request):
    inquiriesList = Inquiries.objects.filter(apartment__seller=request.user, apartment__status=False)
    broker = Broker.objects.filter(user=request.user).first()  # מחזיר None אם אין התאמה
    benefits = broker.benefits if broker else None
    data = {
        'Inquiries': inquiriesList,
        'benefits': benefits
    }
    return render(request, 'InquiriesList.html', data)


@login_required
def buy(request, id):
    if request.method == 'POST':
        try:
            a = Apartment.objects.get(id=id)
            a.status = True
            if a.brokerage:
                broker = Broker.objects.filter(user=a.seller).first()  # מחזיר None אם לא נמצא
                if broker:
                    broker.benefits += a.price / 50
                    broker.save()
                else:
                    print(f"Broker for seller {a.seller} does not exist.")
            a.save()
        except Apartment.DoesNotExist:
            print(f"Apartment with id {id} does not exist.")
    return redirect('/app1/apartment')
