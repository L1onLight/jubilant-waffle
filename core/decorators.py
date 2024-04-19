from django.shortcuts import redirect


def logout_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Replace 'logout' with the appropriate URL name or path
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper


def login_required_my(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Replace 'logout' with the appropriate URL name or path
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper
