from django import forms

from main.models import *


class StyleForMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MessageForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'context')


class MailingForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('mailing_time', 'periodicity', 'mailing_status', 'is_active', 'client')


class ClientForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email')


class BlogForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'is_public')
