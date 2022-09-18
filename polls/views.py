
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.db.models import F
from django.utils import timezone

from django.contrib.auth.decorators import login_required, permission_required

from .models import Question, Choice

from .forms import FormCreateQuestion, FormCreateChoice

# My functions
def isOwnerQuestion(request, topic):
    return request.user == topic.owner

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.all().filter(pub_date__lte=timezone.now(), private_question=False)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail_question.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.all().filter(pub_date__lte=timezone.now())

  
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results_question.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.all().filter(pub_date__lte=timezone.now())
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail_question.html', {
            'question': question,
            'error_message': "You didn't select a choice.", })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def create_question(request):
    if request.method == 'POST':
        form = FormCreateQuestion(data=request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = request.POST['pub_date']
            question.owner = request.user
            question.save()
            form.save()

            return HttpResponseRedirect(reverse('polls:index'))

    form = FormCreateQuestion()

    template_name = 'polls/add_question.html'
    context = {
        'form':form}
    
    return render(request, template_name=template_name, context=context)

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if isOwnerQuestion(request, question):
        if request.method == 'POST':
            # verified forms
            form = FormCreateQuestion(instance=question, data=request.POST)

            if form.is_valid():
                form.save()

                return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

        
        form = FormCreateQuestion(instance=question)

        template_name = 'polls/edit_question.html'
        context = {
            'question':question,
            'form':form,
            }
        
        return render(request, template_name=template_name, context=context)
    return HttpResponse("Not allowed!")

@login_required
def delete_question(request, question_id):
    
    question = Question.objects.get(pk=question_id)
    if isOwnerQuestion(request, question):
        question.delete()
        return HttpResponseRedirect(reverse('polls:index'))
    return HttpResponse("Not allowed")

@login_required
def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if isOwnerQuestion(request, question):

        if request.method == 'POST':
            # verified forms
            form = FormCreateChoice(data=request.POST)
            if form.is_valid():
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
                return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

        form = FormCreateChoice()

        template_name = 'polls/add_choice.html'
        context = {
            'question':question,
            'form':form,}

        return render(request, template_name=template_name, context=context)
    else:
        return HttpResponse("Not allowed!")