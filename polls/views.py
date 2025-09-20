from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic

from .models import Questions, Choice

# All Views are here 
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Questions.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Questions
    template_name = "polls/details.html"

class ResultView(generic.DetailView):
    model = Questions
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.Post["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))