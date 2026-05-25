from django.shortcuts import render, redirect
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from .models import Document
import fitz
import google.generativeai as genai 
from django.conf import settings

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
    documents = Document.objects.filter(user=request.user)

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
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    Summarize the following study material in simple student-friendly language.
    Text:
    {text[:10000]}
    """
    response = model.generate_content(prompt)
    return response.text