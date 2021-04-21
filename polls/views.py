from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import JsonResponse

from .models import Question, Choice, Answer




def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'sondage/index.html', context)

def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, 'sondage/detail.html', { 'question': question })

def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  exist = False
  for i in Answer.objects.filter(question=question):
      if request.user == i.organisme:
          exist = True
  print(exist)
  return render(request, 'sondage/results.html', { 'question': question,'exist':exist })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'sondage/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        exist = False
        for i in Answer.objects.filter(question=question):
            if request.user == i.organisme:
                exist=True
        if exist==False:
            selected_choice.votes += 1
            selected_choice.save()
            Answer.objects.create(organisme=request.user, question=question, choice=selected_choice)

            # HTTPRESPONSE bech ki yaamel back fel navigateur metaawadech tebaath

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        else:
            return render(request, 'sondage/detail.html', {
                'question': question,
                'error_message': "You already voted!"})

# EL DATA JSON MTAI
def resultsData(request, obj):
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.votes})
    print('t',votedata)
    return JsonResponse(votedata, safe=False)


