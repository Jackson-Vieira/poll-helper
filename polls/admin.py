from django.contrib import admin
from polls.models import Choice, Poll, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Privacidade', {'fields':[
            'owner']}),

        ('Informações relevantes', {'fields':[
            'poll_name', 'openvot', 'poll_type', 'poll_info_url', 'randomize_choice_order',]}),

        ('Datas/Agendamentos', {'fields':[
            'voting_starts_at', 'voting_ends_at', ]}),
    ]

    list_display = ['poll_name', 'created', ]
    list_filter = ['created']
    search_fields = ['poll_name']

    date_hierarchy = 'created'

    inlines = [ChoiceInline,]

admin.site.register(Poll, PollAdmin)
admin.site.register(Vote)