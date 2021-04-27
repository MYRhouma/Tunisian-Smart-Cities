from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import JsonResponse

from .models import Question, Choice, Answer




def index(request):
    VOTE=True
    onlineUser = request.user
    from account.models import Message, Organisme
    messaget = Message.objects.filter(reciever=onlineUser, viewed=False)[:3]
    messagetMetakrawech = messaget.count()
    DATA = dict()
    organismes = Organisme.objects.all()
    categories = list(org.category for org in organismes)
    unique_list = []
    for x in categories:
        if x not in unique_list:
            unique_list.append(x)
    for i in range(len(unique_list)):
        cat = unique_list[i]
        DATA[cat] = Organisme.objects.filter(category=cat).count()
    max = Question.objects.count()
    nombre= Answer.objects.filter(organisme=request.user).count()
    pourcentage = int(nombre/max*100)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list,'pourcentage':pourcentage,'VOTE':VOTE,'onlineUser':onlineUser,'messagetMetakrawech':messagetMetakrawech, 'categories': DATA,}
    return render(request, 'registration/polls.html', context)

def detail(request, question_id):
  VOTE = True
  onlineUser = request.user
  from account.models import Message, Organisme
  messaget = Message.objects.filter(reciever=onlineUser, viewed=False)[:3]
  messagetMetakrawech = messaget.count()
  DATA = dict()
  organismes = Organisme.objects.all()
  categories = list(org.category for org in organismes)
  unique_list = []
  for x in categories:
      if x not in unique_list:
          unique_list.append(x)
  for i in range(len(unique_list)):
      cat = unique_list[i]
      DATA[cat] = Organisme.objects.filter(category=cat).count()
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("La question n'existe pas")
  return render(request, 'registration/detail.html', { 'question': question ,'VOTE':VOTE,'onlineUser':onlineUser,'messagetMetakrawech':messagetMetakrawech, 'categories': DATA,})

def results(request, question_id):
  VOTE = True
  onlineUser = request.user
  from account.models import Message,Organisme
  messaget = Message.objects.filter(reciever=onlineUser, viewed=False)[:3]
  messagetMetakrawech = messaget.count()
  DATA = dict()
  organismes = Organisme.objects.all()
  categories = list(org.category for org in organismes)
  unique_list = []
  for x in categories:
      if x not in unique_list:
          unique_list.append(x)
  for i in range(len(unique_list)):
      cat = unique_list[i]
      DATA[cat] = Organisme.objects.filter(category=cat).count()
  question = get_object_or_404(Question, pk=question_id)
  exist = False
  for i in Answer.objects.filter(question=question):
      if request.user == i.organisme:
          exist = True
  print(exist)
  return render(request, 'registration/results.html', { 'question': question,'exist':exist ,'VOTE':VOTE,'onlineUser':onlineUser,'messagetMetakrawech':messagetMetakrawech, 'categories': DATA,})

def vote(request, question_id):
    VOTE = True
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'registration/detail.html', {
            'question': question,
            'error_message': "Faites un choix.",
            'VOTE':VOTE
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
            return render(request, 'registration/detail.html', {
                'question': question,
                'error_message': "Vous avez deja voté!",'VOTE':True})

# EL DATA JSON MTAI
def resultsData(request, obj):
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.votes})
    print('t',votedata)
    return JsonResponse(votedata, safe=False)


