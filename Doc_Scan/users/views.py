from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from django.http import Http404
from django.db.models import Sum
from django.core.files.storage import default_storage
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .utils import get_openai_similarity

def index(request):
    print("Home")
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)  # Create the user
        user.save()

        CustomUserProfile.objects.create(user=user)

        messages.success(request, "Your account has been created successfully!")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Authenticate user
        if user is not None:
            login(request, user)
            request.session['username'] = user.username  # Store username in session
            request.session['user_id'] = user.id  # Store user ID in session
            messages.success(request, "Login successful!")
            return redirect('home')  # Redirect to home page after login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('forgot_password')

        try:
            user = User.objects.get(username=username, email=email)
            user.set_password(new_password) 
            user.save()
            messages.success(request, "Password reset successful. You can now log in.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "No user found with the provided details.")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')

def home(request):
    pending_count = 0
    pending_requests = [] 

    if request.user.is_authenticated and request.user.is_staff:
        pending_requests = CreditRequest.objects.filter(approved=0)  # Fetch only pending requests
        pending_count = pending_requests.count()
    else:
        index(request)

    return render(request, 'home.html', {'pending_count': pending_count, 'pending_requests': pending_requests})


def Logout(request):
    logout(request)
    return redirect("index")

def about(request):
    return render(request, "about.html")

@login_required
def request_credits(request):
    if request.method == "POST":
        requested_credits = int(request.POST['requested_credits'])
        
        if requested_credits <= 0:
            messages.error(request, "You must request a positive number of credits.")
        else:
            CreditRequest.objects.create(
                user=request.user,
                requested_credits=requested_credits,
            )
            messages.success(request, "Your request for additional credits has been submitted for review.")
        return redirect('home')
    
    return render(request, 'request_credits.html')

@login_required
def credit_requests(request):
    if not request.user.is_staff:
        raise Http404("You do not have permission to view this page.")

    credit_requests = CreditRequest.objects.all().order_by('-created_at')  # Get all credit requests

    return render(request, 'credit_requests.html', {'credit_requests': credit_requests})

@login_required
def approve_credit_request(request, request_id):
    if not request.user.is_staff:
        raise Http404("You do not have permission to approve this request.")

    credit_request = get_object_or_404(CreditRequest, id=request_id)

    if credit_request.approved == 0:  # Only approve if it's still pending
        user = credit_request.user
        requested_credits = credit_request.requested_credits

        user_profile, created = CustomUserProfile.objects.get_or_create(user=user)
        user_profile.add_credits(requested_credits)

        credit_request.approved = 1  # Set to Approved
        credit_request.save()

    return redirect('credit_requests')

@login_required
def deny_credit_request(request, request_id):
    if not request.user.is_staff:
        raise Http404("You do not have permission to deny this request.")

    credit_request = get_object_or_404(CreditRequest, id=request_id)

    if credit_request.approved == 0:  # Only deny if it's still pending
        credit_request.approved = 2  # Set to Denied
        credit_request.save()

    return redirect('credit_requests')


from django.db.models import Sum

@login_required
def user_profile(request):
    if request.user.is_staff:
        # Admin view
        credit_requests = CreditRequest.objects.all()
        total_requests = credit_requests.count()
        total_requested_credits = credit_requests.aggregate(Sum('requested_credits'))['requested_credits__sum'] or 0
        documents = Document.objects.all()  # Fetch all uploaded documents

        context = {
            'credit_requests': credit_requests,
            'total_requests': total_requests,
            'total_requested_credits': total_requested_credits,
            'documents': documents,  # Pass uploaded documents to template
            'is_admin': True,
        }
        return render(request, 'admin_profile.html', context)
    else:
        # Regular user view
        user_profile = CustomUserProfile.objects.get(user=request.user)
        scan_records = ScanRecord.objects.filter(user=request.user)
        credit_requests = CreditRequest.objects.filter(user=request.user)

        for record in scan_records:
            record.match_score = int(record.match_score * 100)


        context = {
            'user_profile': user_profile,
            'scan_records': scan_records,
            'credit_requests': credit_requests,
            'is_admin': False,
        }
        return render(request, 'user_profile.html', context)

@login_required
def upload_document(request):
    if not request.user.is_staff:     # only admin able to upload documents
        messages.error(request, "You do not have permission to upload documents.")
        return redirect('user_profile')

    if request.method == "POST":
        file = request.FILES.get("document")
        if file:
            Document.objects.create(user=request.user, file=file)
            messages.success(request, "Document uploaded successfully!")
    
    return redirect('user_profile')


@login_required
def delete_document(request, doc_id):
    if request.user.is_staff:
        document = get_object_or_404(Document, id=doc_id)
        default_storage.delete(document.file.path)  
        document.delete()  
    return redirect('user_profile')


@login_required
def scanUpload(request):
    if request.method == "POST" and request.FILES.get("document"):
        uploaded_file = request.FILES["document"]
        file_name = uploaded_file.name  # Get the uploaded file name
        user = request.user

        scanned_document = Document.objects.create(user=user, file=uploaded_file)  # Save uploaded document

        user_profile = CustomUserProfile.objects.get(user=user)  # Deduct 1 credit from user
        if user_profile.credits > 0:
            user_profile.credits -= 1
            user_profile.save()
        else:
            return render(request, 'scanUpload.html', {'error': 'Insufficient credits.'})

        temp_path = default_storage.save(f'temp/{uploaded_file.name}', uploaded_file)  # Read uploaded file content
        temp_file_path = os.path.join(settings.MEDIA_ROOT, temp_path)

        try:
            with open(temp_file_path, 'r', encoding='utf-8') as file:
                uploaded_text = file.read()
        except Exception as e:
            return render(request, 'scanUpload.html', {'error': f"Error reading file: {str(e)}"})

        stored_documents = Document.objects.exclude(id=scanned_document.id)  # Retrieve stored documents (excluding the uploaded one)
        stored_texts = []
        stored_doc_ids = []

        for doc in stored_documents:
            try:
                with open(doc.file.path, 'r', encoding='utf-8') as stored_file:
                    stored_texts.append((doc, stored_file.read()))
            except Exception as e:
                print(f"Error reading document {doc.id}: {e}")

        if not stored_texts:  # If no stored documents exist
            return render(request, 'scanUpload.html', {
                'document': scanned_document,
                'similarity_scores': [],
                'error': 'No documents available for comparison.',
                'file_name': file_name
            })

        # Use OpenAI API to compute similarity scores
        similarity_results = []
        for matched_doc, matched_text in stored_texts:
            try:
                similarity_score, similar_text = get_openai_similarity(uploaded_text, matched_text)
            except Exception as e:
                similarity_score, similar_text = 0, "Error extracting similar content."
            
            similarity_results.append((matched_doc, similarity_score, similar_text))
            
            # Store scan record
            ScanRecord.objects.create(
                user=user,
                scanned_document=scanned_document,
                matched_document=matched_doc,
                match_score=similarity_score / 100
            )

            # Store match result in DB
            MatchResult.objects.create(
                scanned_document=scanned_document,
                matched_document=matched_doc,
                similarity_score=similarity_score / 100
            )

        similarity_results.sort(key=lambda x: x[1], reverse=True)
        top_3_matches = similarity_results[:3]

        scan_records = ScanRecord.objects.filter(user=user).order_by('-scanned_at')[:3]

        context = {
            'document': scanned_document,
            'file_name': file_name,
            'similarity_scores': top_3_matches,
            'documents': [doc for doc, _, _ in top_3_matches],  # Only top 3 documents
            'scan_records': scan_records
        }
        return render(request, 'scanUpload.html', context)

    return render(request, 'scanUpload.html')