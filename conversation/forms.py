from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
            'rows': 2,
            'class': 'w-full py-4 px-3 text-gray-700 border rounded-lg focus:outline-none focus:shadow-outline'
            })
        }