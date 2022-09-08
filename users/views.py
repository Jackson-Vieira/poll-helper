from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def register(request):
    if request.method != 'POST':
        form = UserCreationForm()

    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            form.save()
            auth_user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
            login(request, user=auth_user)
            return HttpResponseRedirect(reverse("polls:index"))

    context = {'form':form}
    template_name = "users/register.html"
    return render(request, template_name, context)

def perfil(request):
    pass

def topics(request):
    pass