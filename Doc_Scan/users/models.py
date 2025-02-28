from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Custom user profile linked to Django's default User model
class CustomUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField(default=20)  # Daily free credits
    last_reset = models.DateField(default=now)  # Track last reset date

    def reset_credits(self):
        """Resets credits to 20 if a new day has started."""
        today = now().date()
        if self.last_reset < today:  # Ensures it updates only once per day
            self.credits = 20
            self.last_reset = today
            self.save()
            
    def add_credits(self, additional_credits):
        """Adds credits to the user's balance."""
        self.credits += additional_credits
        self.save() 

# Model for tracking credit requests
class CreditRequest(models.Model):
    STATUS_CHOICES = (
        (0, "Pending"),
        (1, "Approved"),
        (2, "Denied"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_credits = models.IntegerField()
    approved = models.IntegerField(choices=STATUS_CHOICES, default=0)  # Updated field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_approved_display()} ({self.requested_credits} credits)"

# Document model
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Track document scans
class ScanRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scanned_document = models.ForeignKey(Document, related_name="scanned_docs", on_delete=models.CASCADE, null=True, blank=True)  # Allow NULL
    matched_document = models.ForeignKey(Document, related_name="matched_docs", on_delete=models.CASCADE, null=True, blank=True)  # Allow NULL
    scanned_at = models.DateTimeField(auto_now_add=True)
    match_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.scanned_document.file.name if self.scanned_document else 'N/A'} matched with {self.matched_document.file.name if self.matched_document else 'N/A'} ({self.match_score * 100:.2f}%)"


# Store document match results
class MatchResult(models.Model):
    scanned_document = models.ForeignKey(Document, related_name="scanned_doc", on_delete=models.CASCADE)
    matched_document = models.ForeignKey(Document, related_name="matched_doc", on_delete=models.CASCADE)
    similarity_score = models.FloatField()
    matched_at = models.DateTimeField(auto_now_add=True)
