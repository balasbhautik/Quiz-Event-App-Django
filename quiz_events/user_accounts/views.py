from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import get_object_or_404

from user_accounts.models import User
from user_accounts.forms import UserSignupForm, UserLoginForm, UserProfileForm, UserChangePasswordForm

# Create your views here.

def user_signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Account Created Succcessfully.')
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'user_accounts/user_signup.html',{'form':form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,'login successfully.')
                return redirect('/')
            else:
                print("Please enter valid email and password.")
                form.add_error(None, "Invalid email or password. Please try again.")
    else:
        form = UserLoginForm()
    return render(request,'user_accounts/user_login.html',{'form':form})
    

def user_logout(request):
    logout(request)
    return redirect('login')


def user_profile(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Profile Updated Successfully.')

        else:
            user = User.objects.get(id=id)
            form = UserProfileForm(instance=user)
        return render(request, 'user_accounts/user_profile.html', {'form':form})
    else:
        return redirect('login')


def user_change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            form = UserChangePasswordForm(request.POST)
            if form.is_valid():
                current_password = form.cleaned_data.get('current_password')
                new_password = form.cleaned_data.get('new_password')
                confirm_new_password = form.cleaned_data.get('confirm_new_password')

                if not user.check_password(current_password):
                    form.add_error('current_password', 'Current password is incorrect.')
                elif new_password != confirm_new_password:
                    form.add_error('confirm_new_password', 'New passwords do not match.')
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your Password Changed Successfully.')
                    return redirect('home')                  
        else:
            form = UserChangePasswordForm()
        return render(request, 'user_accounts/user_change_pass.html',{'form':form})
    else:
        return redirect('login')