# Credit-Based-Document-Scanning-System

Introduction

The Credit-Based Document Scanning System is a web application built using Django that enables users to efficiently scan and compare documents using AI-powered text similarity analysis. The system follows a credit-based model, where users require credits to perform document scans. It integrates OpenAI API to enhance document comparison accuracy, surpassing traditional TF-IDF and Cosine Similarity techniques.

Features

User Authentication & Role Management

Users can register and log in securely using Django’s built-in authentication.

Two user roles:

Standard User: Can scan documents using available credits.

Admin: Can upload reference documents and manage credit requests.

Credit-Based System

Users receive 20 free credits per day, reset at midnight.

Each document scan deducts 1 credit.

Users can request additional credits from the admin.

AI-Powered Document Scanning

Users can upload plain text documents for comparison.

The system calculates similarity using OpenAI API for higher accuracy.

AI extracts meaningful common content between the uploaded document and reference documents.

User Profile & History

Users can view their credit balance, past document scans, and credit request history.

Admin can manage uploaded documents and track user activities.

Security & Access Control

Passwords are securely hashed using Django’s built-in authentication.

Session-based authentication ensures security.

Access control restricts document scanning to authenticated users with sufficient credits.

Performance Evaluation

Two versions of the system were developed:

Version 1 - Used TF-IDF and Cosine Similarity for initial similarity scoring, then leveraged OpenAI API for detailed content matching.

Version 2 - Fully powered by OpenAI API, achieving higher accuracy in similarity detection.

Comparison Results:

TF-IDF & Cosine Similarity: 36% similarity score with a reference document.

OpenAI API-based Matching: 45% similarity score with the same reference document.

The AI-driven approach significantly improves document comparison accuracy and enhances the overall efficiency of the system.

System Requirements

Hardware Requirements

Processor: Intel Core i5 or AMD Ryzen 5 (or higher)

RAM: Minimum 8GB (16GB recommended)

Storage: 20GB of free space (SSD recommended)

Operating System: Windows 10/11, macOS, or Linux (Ubuntu 20.04+)

Software Requirements

Programming Language: Python 3.10+

Framework: Django 4.x

Frontend: HTML, CSS, JavaScript (Bootstrap)

Database: PostgreSQL 13+ (or any SQL database)

AI & NLP: OpenAI API, Scikit-learn

Installation & Setup

1. Clone the Repository

git clone <repository_link>
cd credit-based-document-scanning

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows

3. Install Dependencies

pip install -r requirements.txt

4. Set Up Environment Variables

Create a .env file and configure your OpenAI API key:

OPENAI_API_KEY='your_openai_api_key'
DJANGO_SECRET_KEY='your_django_secret_key'
DEBUG=True

5. Apply Database Migrations

python manage.py makemigrations
python manage.py migrate

6. Create a Superuser (Admin Access)

python manage.py createsuperuser

7. Run the Django Server

python manage.py runserver

Access the application at http://127.0.0.1:8000/

Future Enhancements

The system has great potential for future improvements, including:

Real-time document scanning for instant results.

Multi-language support for global accessibility.

Advanced AI models for deeper text analysis.

Cloud-based integration for scalability and enhanced storage.

Automated summarization and document classification features.

Conclusion

The Credit-Based Document Scanning System integrates AI-driven document analysis with a structured credit-based model, offering a secure, efficient, and user-friendly solution for document similarity detection. By leveraging the OpenAI API, the system provides superior accuracy compared to traditional text-matching techniques.

With its robust features, including authentication, credit management, scan history tracking, and AI-powered matching, this platform is a valuable tool for various applications such as plagiarism detection, legal document comparison, content validation, and research analysis.

For detailed documentation, please visit the GitHub repository.
