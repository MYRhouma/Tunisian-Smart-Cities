from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from account.forms import DocumentForm, MessageForm, ApplicationForm
from account.models import Message, Organisme, Category, Entity, Application


# Create your views here.
def home(request):
    form =ApplicationForm()
    if request.method=='POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            category=form.cleaned_data['category']
            name=form.cleaned_data['name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            bio=form.cleaned_data['bio']
            message=form.cleaned_data['message']
            a=Application.objects.create(category=category,name=name,username=username,email=email,bio=bio,message=message)
            a.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'home.html',{'form':form})

def dashboard(request):
    messagetMetakrawech= Message.objects.filter(reciever=request.user,viewed = False).count()
    context={'numNotReadMsg':messagetMetakrawech}
    return render(request,'registration/dashboard.html',context)
def messagesInbox(request):
    msgList=Message.objects.filter(reciever = request.user)
    print(msgList)
    for msg in msgList:
        if not msg.viewed:
            msg.viewed = True
            msg.save()
    context={'msgList':msgList}
    return render(request,'message/inbox.html',context)
 
def messagesSent(request):
    msgList=Message.objects.filter(sender = request.user)
    context={'msgList':msgList}
    return render(request,'message/sentbox.html',context)

     
def SendMessage(request):
    user = request.user
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.sender = user
            form.save()
            return redirect('messagesSent')
    else:
        form = MessageForm()
        if not user.is_staff:
            form.fields["reciever"].queryset = Organisme.objects.filter(is_staff=True)
        else:
            form.fields["reciever"].queryset = Organisme.objects.all()
    context = {'form': form}
    return render(request, 'message/sendmessage.html', context)


            


def CategoryList(request):
    categories= Category.objects.all()
    context={'categories':categories,}
    return render(request, "organism/categories.html", context)


def OrganisationsInCategory(request,cat):
    categoryOrgs=Organisme.objects.filter(category=cat)
    context={'cat':cat,'categoryOrgs':categoryOrgs}
    return render(request, "organism/organisationList.html", context)

def EntityInOrganism(request,org):
    OrganismEntity=Entity.objects.filter(organisme=org)
    context={'org':org,'OrganismEntity':OrganismEntity}
    return render(request, "organism/EntityList.html", context)


# DOCUMENT UPLOAD ala site par utilisateur
def DocumentUpload(request):
    if request.method == 'POST':
        user = request.user
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.sender = user
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'document/documentUpload.html', {
        'form': form
    })