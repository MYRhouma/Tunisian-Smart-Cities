from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from account.forms import MessageForm, ApplicationForm,UpdateProfile
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
@login_required()
def dashboard(request):
    DASHBOARD=True
    onlineUser = request.user
    getuser = Organisme.objects.filter(username=onlineUser.username).first()
    messaget= Message.objects.filter(reciever=onlineUser,viewed = False)[:3]
    messagetMetakrawech=messaget.count()
    DATA=dict()
    organismes=Organisme.objects.all()
    categories=list(org.category for org in organismes)
    unique_list = []
    for x in categories:
        if x not in unique_list:
            unique_list.append(x)
    for i in range(len(unique_list)):
        cat=unique_list[i]
        DATA[cat]=Organisme.objects.filter(category=cat).count()
    print(messagetMetakrawech)
    context={'DASHBOARD':DASHBOARD,'numNotReadMsg':messagetMetakrawech,'messaget':messaget,'onlineUser':getuser,'categories':DATA}
    return render(request,'registration/dashboard.html',context)

@login_required()
def CategoryList(request):
    categories= Category.objects.all()
    context={'categories':categories,}
    return render(request, "organism/categories.html", context)

@login_required()
def OrganisationsInCategory(request,cat):
    ORGANISATION=True
    onlineUser = request.user
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
        categ = unique_list[i]
        DATA[categ] = Organisme.objects.filter(category=categ).count()
    print(messagetMetakrawech)
    categoryOrgs = Organisme.objects.filter(category=cat)
    print(categoryOrgs)
    print(cat)
    context = {'numNotReadMsg': messagetMetakrawech, 'messaget': messaget, 'onlineUser': onlineUser, 'categories': DATA,
               'ORGANISATION': ORGANISATION,'cat':cat,'categoryOrgs':categoryOrgs,}
    return render(request, 'registration/dashboard.html', context)

@login_required()
def EntityInOrganism(request,org):
    ENTITY = True
    onlineUser = request.user
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
    print(messagetMetakrawech)
    OrganismEntity = Entity.objects.filter(organisme=org)
    context = {'ENTITY':ENTITY,'org': org, 'OrganismEntity': OrganismEntity,'numNotReadMsg': messagetMetakrawech, 'messaget': messaget, 'onlineUser': onlineUser, 'categories': DATA,
            }
    return render(request, 'registration/dashboard.html', context)


@login_required()
def messagesInbox(request):
    msgList=Message.objects.filter(reciever = request.user)
    print(msgList)
    for msg in msgList:
        if not msg.viewed:
            msg.viewed = True
            msg.save()
    context={'msgList':msgList}
    return render(request,'message/inbox.html',context)


@login_required()
def messagesSent(request):
    msgList=Message.objects.filter(sender = request.user)
    context={'msgList':msgList}
    return render(request,'message/sentbox.html',context)

@login_required()
def SendMessage(request):
    sendmsg=True
    onlineUser = request.user
    getuser = Organisme.objects.filter(username=onlineUser.username).first()
    messaget = Message.objects.filter(reciever=onlineUser, viewed=False)[:3]
    messagetMetakrawech = messaget.count()
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
    context = {'form': form,'sendmsg':sendmsg,'onlineUser':getuser,'messagetMetakrawech':messagetMetakrawech}
    return render(request, 'registration/dashboard.html', context)


            
# class EditProfile(UpdateView):
#     model = Organisme
#     fields = ['name','bio','email','profile_pic']
#     template_name = 'registration/dashboard.html'
#     success_url = reverse_lazy('dashboard')

@login_required()
def EditProfile(request):
    EDITPROFILE=True
    onlineUser = request.user
    getuser = Organisme.objects.filter(username=onlineUser.username).first()
    messaget = Message.objects.filter(reciever=onlineUser, viewed=False)[:3]
    messagetMetakrawech = messaget.count()
    if request.method == 'POST':
        form = UpdateProfile(request.POST,
                                   request.FILES,
                                   instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Modifications effecutées avec succees!')
            return redirect('editprofile')

    else:
        form = UpdateProfile(instance=request.user)
        print(form)
    context = {
        'form_p': form,'EDITPROFILE':EDITPROFILE,'onlineUser':getuser,'messagetMetakrawech':messagetMetakrawech
    }

    return render(request, 'registration/dashboard.html', context)



# DOCUMENT UPLOAD ala site par utilisateur
# @login_required()
# def DocumentUpload(request):
#     if request.method == 'POST':
#         user = request.user
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.sender = user
#             form.save()
#             return redirect('home')
#     else:
#         form = DocumentForm()
#     return render(request, 'document/documentUpload.html', {
#         'form': form
#     })