from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('add_question/', views.create_question, name='add_question'),
    path('edit_question/<int:question_id>',views.edit_question, name='edit_question'),
    path('delete_question/<int:question_id>/',views.delete_question, name='delete_question'),
    path('<int:question_id>/add_choice/',views.add_choice, name='add_choice'),
]