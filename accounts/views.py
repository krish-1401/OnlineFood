from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User,UserProfile
from vendor.forms import VendorForm
from django.contrib import messages
from django.contrib import auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

from django.core.exceptions import PermissionDenied
# Restrict the vendor from accessing the customer page 
# Restrict the customer from accessing the vendor page

def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionError
    
def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionError
    

def registerUser(request):
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            # Hashing the password
            # password=form.cleaned_data['password'] 
            # user=form.save(commit=False)
            # user.set_password(password)
            # user.role=User.CUSTOMER
            # user.save()

            # Create the user using create_user model 
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request,"Your accound has been registered successfully! ")
            return redirect('registerUser')
    else:
        form=UserForm()
    return render(request,'accounts/registerUser.html',{'form':form,})

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are logged in!")
        return redirect('dashboard')
    elif request.method=='POST':
        # store the data and create the user
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,"Your account has been registered succefully! Please wait for the approval.")
            return redirect('registerVendor')
        else:
            print(form.errors)
    else:
        form=UserForm()
        v_form=VendorForm()
    context={
        'form':form,
        'v_form':v_form,
    }
    return render(request,'accounts/registerVendor.html',context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are logged in!")
        return redirect('myAccount')
    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are now logged in.")
            return redirect('myAccount')
        else:
            messages.error(request,"Invalid Login Credentials")
            return redirect('login')
        
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"You are logged out.")
    return redirect('login') 

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custdashboard(request):
    return render(request,'accounts/custdashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect()

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    return render(request,'accounts/vendordashboard.html')
