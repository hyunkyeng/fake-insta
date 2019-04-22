from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required



# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request, 'accounts/signup.html', context)
    
    
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        form = AuthenticationForm()
    context = {'form':form,}
    return render(request, 'accounts/signup.html', context)
    
def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = {'people': people,}
    return render(request, 'accounts/people.html', context)
    
@login_required
def update(request):
    if request.method == 'POST':
        pass
    else:
        user_change_form = UserChangeForm(instance=request.user)
    context = {'user_change_form': user_change_form,}
    return render(request, 'accounts/update.html', context)
    
    

    
    