from django import forms
from account.models import Message, Organisme, Application


# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ('sender','note', 'document', )
#         exclude = ('sender',)


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reciever'].widget.attrs.update({'class': 'form-select'})
    class Meta:
        model = Message
        fields = ('reciever','object','msg_content','document','sender')
        exclude=('sender',)

class LoginForm(forms.ModelForm):
    class Meta:
        model = Organisme
        fields = ('username', 'password', )

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Organisme
        fields = ('name', 'email', 'bio','profile_pic')

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('category', 'name', 'username', 'email', 'bio', 'message')
        exclude = ('accepted',)