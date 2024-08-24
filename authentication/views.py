from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from admin_panel.views import get_user_initials

# Create your views here.

def testing (request):

    user = request.user
    initials = get_user_initials(user)
    
    return render(request, "authentication/test.html",{
        'initials' : initials
    })
    
def in_progress_template(request):
    
    user = request.user
    initials = get_user_initials(user)

    return render(request, "authentication/dummy_template.html",{
        'initials' : initials
    })

def logins(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']

        user = User.objects.filter(username=username).first()
        if user:
            if not user.is_active:
                messages.warning(request, "Not Yet Approved. Contact the Admin")
            else:
                user = authenticate(request, username=username, password=pass1)
                if user is not None:
                    if user.id == 1 or user.is_superuser:
                        login(request, user)
                        return redirect('/admin/dashboard')
                    else:
                        login(request, user)
                        return redirect('/in_progress_template')
                else:
                    messages.warning(request, "Wrong credentials. Please try again.")
        else:
            messages.error(request, "Wrong credentials. Please try again.")
        
        return redirect('/')

    
    return render(request, "authentication/login.html")

def signup(request):
    
    if request.method == 'POST':

        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('/signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email address already exists!')
            return redirect('/signup')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters!')
            return redirect('/signup')

        if not password.isalnum():
            messages.error(request, 'Password must be alphanumeric')
            return redirect('/signup')

        if password == confirm_password:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.is_active = False  

            myuser.save()

            messages.success(request, "Account successfully created")

            return redirect('/')
        
    return render(request, "authentication/register.html")

def signout(request):
    logout(request)
    return redirect('/')