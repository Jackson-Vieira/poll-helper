from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from polls.models import Question

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

@login_required
def topics(request):
    topics = Question.objects.filter(
        owner=request.user,
    )

    template_name = 'users/topics.html'
    context = {'topics':topics}
    return render(request, template_name, context)