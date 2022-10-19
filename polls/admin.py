from django.contrib import admin

from polls.models import Choice, Topic, Registry

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Privacidade', {'fields':['owner']}),
        (None, {'fields':['topic_text']}),
    ]

    list_display = ['question_text', 'pub_date', 'was_published_recently']
    list_filter = ['created']
    search_fields = ['question_text']

    date_hierarchy = 'pub_date'

    inlines = [ChoiceInline,]


admin.site.register(Topic, TopicAdmin)
admin.site.register(Registry)
