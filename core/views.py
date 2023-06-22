from django.shortcuts import render
from user.forms import RegisterForm
# Create your views here.


def home(request):
    context = {'form': RegisterForm}
    return render(request, 'core/index.html', context)


def reg_page(request):
    return render(request, 'core/index.html')
