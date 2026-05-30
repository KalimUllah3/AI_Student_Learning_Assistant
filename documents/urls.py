from django.urls import path
from .views import upload_document, document_list, ask_question

urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path('documents/', document_list, name='document_list'),
    path('ask/<int:document_id>/', ask_question, name='ask_question'),
]