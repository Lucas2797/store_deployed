from django.shortcuts import redirect, render
from django.http import HttpResponse


def allowed_users(allowed_ones=[]):
    def decorator(view_func):
        def func_wrapper(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group =  request.user.groups.all()[0].name
            
            if group in allowed_ones:
                return view_func(request, *args, **kwargs)

            else:
                return redirect('login')
        return func_wrapper
    return decorator


def already_authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('../../products/home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func