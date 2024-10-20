from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from core.models import *
# Create your views here.
def user_login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        messages.info(request,"Login Failed,Please try again")
    return render(request,'accounts/login.html')
def user_register(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        age=request.POST.get('age')
        address=request.POST.get('address')
        city=request.POST.get('city')
        zip_code=request.POST.get('zipcode')
        gender = request.POST.get('gender') 
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        phone_field=request.POST.get('phone_field')
        # print(username,email)
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists!")
                return redirect('user_register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request,"email already exists!")
                    return redirect('user_register')
                else:
                    user=User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    data=Customer(user=user,firstname=firstname,lastname=lastname,phone_field=phone_field,age=age,gender=gender,address=address,city=city,zip_code=zip_code)
                    data.save()
                    # code for login  of user will come here
                    our_user=authenticate(username=username,password=password)
                    if our_user is not None:
                        login(request,user)
                        return redirect('/')
        else:
            messages.info(request,"Password and Confirm Password Missmatch!")
            return redirect('user_register')
    return render(request,'accounts/register.html')
def user_logout(request):
    logout(request)
    return redirect('/')
