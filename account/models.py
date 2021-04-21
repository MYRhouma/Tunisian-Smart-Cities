from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
import django.contrib.auth
from django.core.exceptions import ObjectDoesNotExist
from tinymce.models import HTMLField


class Category(models.Model):
    name=models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return str(self.id)+'# '+str(self.name)


class Application(models.Model):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    bio=models.TextField(max_length=600,blank=True)
    category=models.ForeignKey(Category,on_delete=models.DO_NOTHING,null=True)
    name=models.CharField(max_length=30,null=True,help_text='Fill name and username will get prefilled with no spaces.')
    email = models.EmailField(blank=False)
    message = models.TextField(blank=True,null=True)
    accepted = models.BooleanField(default=False,blank=True,null=False,help_text='Check this field to create an account with this model\'s data.')
    def __str__(self):
        return self.name



class Organisme(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and no spaces! fill name and let this field get prefilled.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    bio=models.TextField(max_length=600,blank=True)
    category=models.ForeignKey(Category,on_delete=models.DO_NOTHING,null=True)
    name=models.CharField(max_length=30,help_text='Fill name and username will get prefilled with no spaces.',null=True)
    email = models.EmailField(_('email address'), blank=False,help_text='You must fill this void to send the email with the random password.')
    first_name = None
    last_name = None
    groups= None
    user_permissions=None
    class Meta:
        verbose_name_plural = "Organisms"
        verbose_name = "Organism"

        
        
class Entity(models.Model):
    organisme = models.ForeignKey(Organisme,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=80)
    function = models.CharField(max_length=60,null=True)
    email=models.EmailField()
    phone=models.IntegerField()
    class Meta:
        verbose_name_plural = "Entities"
    def __str__(self):
        return str(self.organisme)+" | "+ self.full_name
    
    
        
class Message(models.Model):
     sender = models.ForeignKey(Organisme, related_name="sender",on_delete=models.CASCADE)
     reciever = models.ForeignKey(Organisme, related_name="receiver",on_delete=models.CASCADE)
     msg_content = models.TextField(max_length=1200)
     created_at = models.DateTimeField(auto_now_add=True)
     viewed = models.BooleanField(default=False)
     def __str__(self):
         return 'From : '+str(self.sender)+' | To : '+str(self.reciever)+str(' | Date : ')+str(self.created_at.date())

        

class Document(models.Model):
    sender = models.ForeignKey(Organisme,on_delete=models.DO_NOTHING,null=True)
    note = models.TextField(max_length=2053,null=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.username

# @receiver(pre_save, sender=Organisme)
# def my_callback(sender, instance, *args, **kwargs):
#     count=len(Organisme.objects.filter(username=instance.username))
#     print('count org',count)
#     if instance.username and instance.email and not instance.is_superuser and count==0:
#         random_password = get_random_string(length=8)
#         instance.set_password(random_password)
#
#         email_body = f"Hello '{instance.name}' your login informations,\nusername: {instance.username} \npassword : {random_password}\n"
#         recips = [instance.email,]
#         print(recips)
#         send_mail(
#             f"{instance.email} welcome",
#             email_body,
#             "mylord5518@gmail.com",
#             recips,
#             fail_silently=False,
#         )
#         print(random_password)
#         print(instance.password)

@receiver(post_save, sender=Organisme)
def admin_creation(sender, instance, *args, **kwargs):
    count=len(Admin.objects.filter(user=instance))
    print(count)
    if (instance.is_superuser or instance.is_staff) and count==0:
        print('admin!!!!!!')
        Admin.objects.create(user=instance)
        # a.save()



@receiver(post_save, sender=Application)
def create_organisation(sender, instance, *args, **kwargs):
    Organisme = django.contrib.auth.get_user_model()
    NoUser=False
    try:
        Organisme.objects.get(username=instance.username)
    except ObjectDoesNotExist:
        NoUser=True
        print('cbon')
    if instance.accepted and NoUser:
        Organisme.objects.create_user(category=instance.category,name=instance.name,username=instance.username,email=instance.email,bio=instance.bio,is_superuser=False,is_staff=False)
        print('compte crée!')


@receiver(pre_save, sender=Message)
def my_callback(sender, instance, *args, **kwargs):
    if instance.sender and instance.reciever and instance.msg_content:
        email_body = f"{instance.sender} has sent you a message,\n message: {instance.msg_content} \n"
        recips = [i.email for i in Organisme.objects.filter(username=instance.reciever) if i.email]
        print(recips)
        send_mail(
            f"{instance.sender} has sent you a message! ",
            email_body,
            "mylord5518@gmail.com",
            recips,
            fail_silently=False,
        )
        print('message en envoyé !')


class Admin(models.Model):
    user = models.OneToOneField(Organisme,on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return str(self.user.username)
ARTICLESTATUS=(
    ("Publish","Publish"),
    ("Brouillon", "Brouillon"),
)
ODIENCESTATUS=(
    ("Define Later","Define Later"),
    ("Private","Private"),
    ("Public", "Public"),
)
class Article(models.Model):
    author = models.ForeignKey(Admin,on_delete=models.CASCADE)
    title = models.CharField(max_length=225,null=True,blank=False)
    # content = models.TextField(max_length=5000,null=True,blank=False)
    content = HTMLField(null=True)
    status = models.CharField(choices=ARTICLESTATUS,max_length=60,default="Brouillon")
    odience = models.CharField(choices=ODIENCESTATUS,max_length=60,default="Define Later")
    published_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return 'Title : '+str(self.title)+' | Author : '+str(self.author.user.name)