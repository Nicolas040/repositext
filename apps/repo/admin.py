from django.contrib import admin
from .models import Document, Folder, DocumentVersion


admin.site.register(Document)
admin.site.register(Folder)
admin.site.register(DocumentVersion)
