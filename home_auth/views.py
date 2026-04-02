from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from django.http import HttpResponse


# -------------------------
# FORGOT PASSWORD (simple placeholder)
# -------------------------
def forgot_password_view(request):
    return HttpResponse("Forgot Password Page")


# -------------------------
# SIGNUP
# -------------------------
def signup_view(request):
    if request.method == 'POST':
                                                                                                                   
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        password   = request.POST.get('password')
        Confirm_Password = request.POST.get('confirm_password')
        role       = request.POST.get('role')

        # Vérification rôle
        if password != Confirm_Password:
            messages.error(request, "you used tow difrent passwords")
            return redirect('signup')

        # Création utilisateur
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        # Attribution des rôles
        user.is_student = (role == 'student')
        user.is_teacher = (role == 'teacher')
        user.is_admin   = (role == 'admin')

        user.save()

        login(request, user)
        messages.success(request, 'Signup successful!')

        return redirect('index')
    else:
     return render(request, 'authentication/register.html')


# -------------------------
# LOGIN
# -------------------------
def login_view(request):
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            

            # Redirection selon rôle
            if user.is_admin:
                return redirect('index')
            elif user.is_teacher:
                return redirect('index')
            elif user.is_student:
                return redirect('signup')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('login')

        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'authentication/login.html')


# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')