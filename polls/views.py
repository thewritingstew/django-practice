from django.http import HttpResponse # not needed once views use render
from django.template import loader # not needed once views use render

from django.http import Http404 # added for step 3? in tutorial
from django.shortcuts import get_object_or_404 # added for step 3? in tutorial
from django.shortcuts import render # added for step 3? in tutorial

from django.http import HttpResponseRedirect # added for step 4 in tutorial
from django.urls import reverse # added for step 4 in tutorial

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_question_list':latest_question_list }

    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})
#    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This preventns data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect (reverse('polls:results', args=(question.id,)))
