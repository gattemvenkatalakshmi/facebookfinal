from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm, UserFormToExcludeFields
from django.contrib.auth.hashers import make_password,check_password


# Create your views here.
def login_page(request):

    form = UserFormToExcludeFields()
    if request.method =='GET':
        return render(request, 'facebook/login.html', {'form': form})

    if request.method == 'POST':
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email_address=email_address)
        except User.DoesNotExist:
            return render(request, 'facebook/login.html', {'message': 'Email does not exist'})

        if check_password(password, user.password):

            return render(request, 'facebook/home.html', {'user': user})
        else:
            return render(request, 'facebook/login.html', {'message': 'Incorrect Password'})
        
    return render(request, 'facebook/login.html', {'form': form})


def signup(request):
    form = UserForm()
    if request.method =='GET':
        return render(request, 'facebook/signup.html', {'form': form})

    if request.method == 'POST':
       
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'facebook/signup.html',{'form': form})
        

    return render(request, 'facebook/signup.html', {'form': form})
def forgot_password(request):
    form = UserForm()
    if request.method =="POST":
        email_address = request.POST.get('email_address')
        password=request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        try:
            user = User.objects.get(email_address=email_address)
            if password == confirm_password:
                hashed_password = make_password(password)
                user.password = hashed_password
                user.save()
                
                return redirect('login')
            else:
                return render(request, 'facebook/forgot_password.html', {'message': 'Different Password'})
        
        except User.DoesNotExist:
            return render(request, 'facebook/forgot_password.html', {'message': 'Email does not exist'})
        

        
       
    return render(request,'facebook/forgot_password.html',{'form': form})
