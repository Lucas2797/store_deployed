from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import UserLoginForm, UserRegisterForm, AutomaticUser
from django.contrib.auth.decorators import login_required
from products.models import Produto
from django.urls import reverse_lazy, reverse
from .decorators import already_authenticated_user, allowed_users
from django.contrib.auth.models import Group



@already_authenticated_user
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/products/home')

    context = {
        'form': form,
    }
    return render(request, "admin/login.amp.html", context)

@allowed_users(allowed_ones=['Admin'])
def register_view(request):
    group = Group.objects.get(name='Vendedor')
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        user.groups.add(group)
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('../../products/admin')

    context = {
        'form': form,
    }
    if request.user_agent.is_mobile:
        return render(request, "admin_amp/signup.amp.html", context)
    elif request.user_agent.is_pc:
        return render(request, "admin/signup.amp.html", context)
    else:
        return render(request, "admin_amp/signup.amp.html", context)


def automatic_view(request):
    group = Group.objects.get(name='Cliente')
    form = AutomaticUser(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password("pass")
        user.save()
        user.groups.add(group)
        new_user = authenticate(username=user.username, password="pass")
        login(request, new_user)
        return redirect('../../products/home')
    if request.user_agent.is_mobile:
        return render(request, "amp/automatic.amp.html", {'form': form})
    elif request.user_agent.is_pc:
        return render(request, "desktop/automatic.amp.html", {'form': form})
    else:
        return render(request, "amp/automatic.amp.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('../login')



