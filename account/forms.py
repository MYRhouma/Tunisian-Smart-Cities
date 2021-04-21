from django import forms
from account.models import Document, Message, Organisme, Application


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('sender','note', 'document', )
        exclude = ('sender',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('reciever','msg_content','sender')
        exclude=('sender',)

class LoginForm(forms.ModelForm):
    class Meta:
        model = Organisme
        fields = ('username', 'password', )

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('category', 'name', 'username', 'email', 'bio', 'message')
        exclude = ('accepted',)