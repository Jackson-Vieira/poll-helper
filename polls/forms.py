from django.forms import ModelForm

from polls.models import Choice, Question


class FormCreateQuestion(ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date')
        labels = {'question_text':'Question text', 
        'pub_date':'Date published'}

    
class FormCreateChoice(ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)
        labels = {'choice_text':'Choice text',}
