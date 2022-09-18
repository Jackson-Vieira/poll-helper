from traceback import format_stack
from django import forms

from polls.models import Choice, Question

class FormCreateQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'private_question')
        labels = {'question_text':'Question text', 'private_question':'Private question'}

    
class FormCreateChoice(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)
        labels = {'choice_text':'Choice text',}
