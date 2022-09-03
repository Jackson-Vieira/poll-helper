from django.contrib import admin

from polls.models import Choice, Question

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Data informations', {'fields':['pub_date']})    
        ]


    list_display = ['question_text', 'pub_date', 'was_published_recently']
    list_filter = ['pub_date']
    search_fields = ['question_text']

    date_hierarchy = 'pub_date'

    inlines = [ChoiceInline,]


admin.site.register(Question, QuestionAdmin)