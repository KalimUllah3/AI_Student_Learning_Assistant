from django.contrib import admin
from .models import Document, QuestionAnswer

# admin.site.register(Document)
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    fields = (
        'title',
        'user',
        'file',
        'extracted_text',
        'summary'
    )
@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display= ('document','question')