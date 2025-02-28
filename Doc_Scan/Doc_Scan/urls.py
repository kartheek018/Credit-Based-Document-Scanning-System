"""Doc_Scan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("index", views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('request_credits/', views.request_credits, name='request_credits'),
    path("Logout", views.Logout, name="Logout"),
    path('credit_requests/', views.credit_requests, name='credit_requests'),
    path('approve/<int:request_id>/', views.approve_credit_request, name='approve_credit_request'),
    path('deny/<int:request_id>/', views.deny_credit_request, name='deny_credit_request'),
    path('profile/', views.user_profile, name='user_profile'),
    path('upload_document/', views.upload_document, name='upload_document'),
    path('delete_document/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('scanUpload/', views.scanUpload, name='scanUpload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
