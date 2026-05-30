from django.urls import path
from .views import upload_document, document_list, ask_question, question_history, generate_document_quiz

urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path('documents/', document_list, name='document_list'),
    path('ask/<int:document_id>/', ask_question, name='ask_question'),
    path('history/', question_history, name='question_history'),
    path('quiz/<int:document_id>/', generate_document_quiz, name='generate_quiz'),
]