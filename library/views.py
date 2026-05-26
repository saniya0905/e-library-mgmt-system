from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Book, Category
from django.contrib.auth import authenticate, login, logout
from .models import Book, Bookmark, Category
from django.contrib import messages
from django.http import JsonResponse
from .models import ReadingHistory
import json
from.models import FavoriteBook, Book

def home(request):
    return render(request, 'library/home.html')


def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        if password != confirm_password:
            messages.error(
                request,
                "Password and Confirm Password do not match"
            )
            return redirect('register')

        # Check username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        # Create User Profile
        UserProfile.objects.create(
            user=user,
            role=role
        )

        messages.success(request, 'Registration Successful')
        return redirect('login')

    return render(request, 'library/register.html')

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid Username or Password')

    return render(request, 'library/login.html')

def explore(request):
    return render(request, 'library/explore.html')

# CATEGORY BOOK PAGES

def programming_books(request):
    return render(request, 'library/programming_books.html')


def literature_books(request):
    return render(request, 'library/literature_books.html')


def science_books(request):
    return render(request, 'library/science_books.html')


def business_books(request):
    return render(request, 'library/business_books.html')

def engineering_books(request):
    return render(request, 'library/engineering_books.html')


def history_books(request):
    return render(request, 'library/history_books.html')

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    profile = UserProfile.objects.get(user=request.user)

    # ADMIN DASHBOARD
    if profile.role == 'ADMIN':

        total_books = Book.objects.count()

        total_students = UserProfile.objects.filter(
            role='STUDENT'
        ).count()

        total_librarians = UserProfile.objects.filter(
            role='LIBRARIAN'
        ).count()

        total_categories = Category.objects.count()

        context = {
            'total_books': total_books,
            'total_students': total_students,
            'total_librarians': total_librarians,
            'total_categories': total_categories,
        }

        return render(
            request,
            'library/admin_dashboard.html',
            context
        )

    # LIBRARIAN DASHBOARD
    elif profile.role == 'LIBRARIAN':

        total_books = Book.objects.count()

        total_categories = Category.objects.count()

        students_reading = ReadingHistory.objects.values(
            'student'
        ).distinct().count()

        context = {
            'total_books': total_books,
            'total_categories': total_categories,
            'students_reading': students_reading,
        }

        return render(
            request,
            'library/librarian_dashboard.html',
            context
        )

    # STUDENT DASHBOARD
    elif profile.role == 'STUDENT':

        reading_count = Bookmark.objects.filter(
            user=request.user,
            completed=False
        ).count()

        completed_count = Bookmark.objects.filter(
            user=request.user,
            completed=True
        ).count()

        favorite_count = FavoriteBook.objects.filter(
            student=request.user
        ).count()

        context = {
            'reading_count': reading_count,
            'completed_count': completed_count,
            'favorite_count': favorite_count,
        }

        return render(
            request,
            'library/student_dashboard.html',
            context
        )
    

def manage_books(request):

    books = Book.objects.all()

    context = {
        'books': books
    }

    return render(
        request,
        'library/manage_books.html',
        context
    )

def edit_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":

        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')

        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES.get('cover_image')

        if request.FILES.get('book_pdf'):
            book.book_pdf = request.FILES.get('book_pdf')

        book.save()

        return redirect('manage_books')
    return render(
        request,
        'library/edit_book.html',
        {'book': book}
    )

def manage_students(request):

    students = UserProfile.objects.filter(
        role='STUDENT'
    )

    context = {
        'students': students
    }

    return render(
        request,
        'library/manage_students.html',
        context
    )


def manage_librarians(request):

    librarians = UserProfile.objects.filter(
        role='LIBRARIAN'
    )

    context = {
        'librarians': librarians
    }

    return render(
        request,
        'library/manage_librarians.html',
        context
    )


def manage_categories(request):

    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(
        request,
        'library/manage_categories.html',
        context
    )

def edit_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":

        category.name = request.POST.get('name')

        category.save()

        return redirect('manage_categories')
    return render(
        request,
        'library/edit_category.html',
        {
            'category': category
        }
    )
def librarian_dashboard(request):

    reading_history = ReadingHistory.objects.select_related(
        'student',
        'book'
    ).order_by('-last_read')

    return render(
        request,
        'library/librarian_dashboard.html',
        {
            'reading_history': reading_history
        }
    )

# LIBRARIAN PAGES

def upload_books(request):

    categories = Category.objects.all()

    if request.method == 'POST':

        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        category_id = request.POST.get('category')

        cover_image = request.FILES.get('cover_image')
        book_pdf = request.FILES.get('book_pdf')

        category = Category.objects.get(id=category_id)
        Book.objects.create(
            title=title,
            author=author,
            description=description,
            category=category,
            cover_image=cover_image,
            book_pdf=book_pdf
        )

        return redirect('upload_books')

    books = Book.objects.all()

    context = {
        'books': books,
        'categories': categories
    }
    return render(
        request,
        'library/upload_books.html',
        context
    )


def librarian_categories(request):

    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(
        request,
        'library/librarian_categories.html',
        context
    )


def student_records(request):

    students = UserProfile.objects.filter(
        role='STUDENT'
    )

    context = {
        'students': students
    }

    return render(
        request,
        'library/student_records.html',
        context
    )

def student_library(request):

    categories = Category.objects.all()

    category_name = request.GET.get('category')

    if category_name:
        books = Book.objects.filter(
            category__name=category_name
        )
    else:
        books = Book.objects.all()

    favorites = FavoriteBook.objects.filter(
        student=request.user
    )

    favorite_ids = favorites.values_list(
        'book_id',
        flat=True
    )

    context = {
        'books': books,
        'categories': categories,
        'favorite_ids': favorite_ids
    }

    return render(
        request,
        'library/student_library.html',
        context
    )

def bookmarks(request):

    if not request.user.is_authenticated:
        return redirect('login')

    user_bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related('book')

    context = {
        'bookmarks': user_bookmarks
    }

    return render(
        request,
        'library/bookmarks.html',
        context
    )

def add_bookmark(request, book_id):

    if not request.user.is_authenticated:
        return redirect('login')

    book = Book.objects.get(id=book_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        book=book
    )

    if created:
        bookmark.current_page = 1
        bookmark.save()

        messages.success(
            request,
            'Book added to bookmarks successfully'
        )

    else:

        messages.info(
            request,
            'Book already bookmarked'
        )

    return redirect('bookmarks')

def save_progress(request, book_id):

    if request.method == "POST":

        page = request.POST.get("page")

        book = Book.objects.get(id=book_id)

        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            book=book
        )

        bookmark.current_page = page
        bookmark.save()

        return JsonResponse({
            'status': 'success'
        })
    
def save_page(request):

    if request.method == "POST":

        data = json.loads(request.body)

        book_id = data.get("book_id")
        page = data.get("page")

        # Bookmark update
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            book_id=book_id
        )

        bookmark.current_page = page
        bookmark.save()

        # Reading history update
        ReadingHistory.objects.update_or_create(
            student=request.user,
            book_id=book_id,
            defaults={
                "current_page": page
            }
        )

        return JsonResponse({
            "status": "saved"
        })
    
def read_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        book=book
    )

    return render(
        request,
        "library/read_book.html",
        {
            "book": book,
            "bookmark": bookmark
        }
    )

def reading_progress(request):

    bookmarks = Bookmark.objects.filter(
        user=request.user
    )

    context = {
        'bookmarks': bookmarks
    }

    return render(
        request,
        'library/reading_progress.html',
        context
    )

def open_book(request, book_id):

    book = Book.objects.get(id=book_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        book=book
    )

    ReadingHistory.objects.update_or_create(
        student=request.user,
        book=book,
        defaults={
            'current_page': bookmark.current_page
        }
    )

    return redirect(book.book_pdf.url)

def reading_activity(request):

    activities = ReadingHistory.objects.select_related(
        'student',
        'book'
    ).order_by('-last_read')

    return render(
        request,
        'library/reading_activity.html',
        {
            'activities': activities
        }
    )

def toggle_favorite(request, book_id):

    book = Book.objects.get(id=book_id)

    favorite = FavoriteBook.objects.filter(
        student=request.user,
        book=book
    ).first()

    if favorite:
        favorite.delete()
    else:
        FavoriteBook.objects.create(
            student=request.user,
            book=book
        )

    return redirect('student_library')

def favorite_books(request):

    favorites = FavoriteBook.objects.filter(
        student=request.user
    )

    return render(
        request,
        'library/favorite_books.html',
        {
            'favorites': favorites
        }
    )


def logout_view(request):
    logout(request)
    return redirect('home')