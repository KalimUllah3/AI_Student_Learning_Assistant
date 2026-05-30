from django.shortcuts import render, redirect
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
import fitz
from google import genai
from django.conf import settings
from .forms import QuestionForm
from .models import Document, QuestionAnswer, Quiz

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            text = extract_text_from_pdf(document.file.path)
            document.extracted_text = text
            document.save()
            summary = generate_summary(text)
            document.summary = summary
            document.save()
            return redirect('upload_document')
    else:
        form = DocumentForm()
    return render(request, 'documents/upload.html', {'form': form})

def document_list(request):
    print("USER:", request.user)
    documents = Document.objects.filter(user=request.user)
    print("DOC COUNT:", documents.count())
    return render(
        request,
        'documents/document_list.html',
        {'documents': documents}
    )
def extract_text_from_pdf(pdf_path):
    text = ""
    pdf = fitz.open(pdf_path)
    for page in pdf:
        text += page.get_text()
    pdf.close()
    return text
def generate_summary(text):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    prompt = f"""
    Summarize the following study material in simple student-friendly language.
    Text:{text[:10000]} """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def answer_question(context, question):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    prompt = f"""
    You are a study assistant.
    Use ONLY the provided document content.
    Document:
    {context[:10000]}
    Question:
    {question}
    If the answer is not present in the document,
    say:
    "This information is not available in the document."
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def ask_question(request, document_id):
    document = Document.objects.get(id=document_id)
    answer = None
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = answer_question(
                document.extracted_text,
                question
            )
            QuestionAnswer.objects.create(
                document=document,
                question=question,
                answer=answer
            )
    else:
        form = QuestionForm()
    return render(
        request,
        'documents/ask_question.html',
        {
            'document': document,
            'form': form,
            'answer': answer
        }
    )

@login_required
def question_history(request):

    questions = QuestionAnswer.objects.filter(
        document__user=request.user).order_by('-id')
    return render(request,'documents/question_history.html',
        { 'questions': questions })

def generate_quiz(text):
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )
    prompt = f"""
    Generate 5 multiple-choice questions (MCQs)
    from the following study material.
    Include:
    - Question
    - 4 options
    - Correct Answer
    Text:
    {text[:10000]}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

@login_required
def generate_document_quiz(request, document_id):
    document = Document.objects.get(id=document_id)
    quiz_text = generate_quiz(
        document.extracted_text
    )
    quiz = Quiz.objects.create(
        document=document,
        quiz_text=quiz_text
    )
    return render(
        request,
        'documents/quiz.html',
        {
            'quiz': quiz
        }
    )
