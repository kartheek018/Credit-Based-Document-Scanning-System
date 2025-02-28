from django.contrib import admin

# Register your models here.
from .models import CustomUserProfile, CreditRequest, Document, ScanRecord, MatchResult

admin.site.register(CustomUserProfile)
admin.site.register(CreditRequest)
admin.site.register(Document)
admin.site.register(ScanRecord)
admin.site.register(MatchResult)
