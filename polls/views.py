from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        """ return latest 5 published question """
        return Question.objects.order_by('-pub_date')[:5]

# def index(request):
#     latest_questions = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_questions': latest_questions
#     }
#     return render(request, 'polls/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You should choose a vote choice.",
        })

    choice.votes = F('votes') + 1
    choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
