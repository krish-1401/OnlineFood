from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User

from django.contrib import messages
# Create your views here.
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