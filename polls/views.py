# from django.http import HttpResponse # not needed once views use render
# from django.template import loader # not needed once views use render
# from django.http import Http404 # added for step 3? in tutorial # not needed starting in 4

from django.shortcuts import get_object_or_404 # added for step 3? in tutorial
from django.shortcuts import render # added for step 3? in tutorial

from django.http import HttpResponseRedirect # added for step 4 in tutorial
from django.urls import reverse # added for step 4 in tutorial
from django.views import generic # added for step 4 in tutorial
from django.utils import timezone # added for step 5 in tutorial

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions, not including those to be
        published in the future.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Exclude detail for questions that have pub_date in future.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Exclude results for questions with pub_date in future.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

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
