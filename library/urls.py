from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('explore/', views.explore, name='explore'),
    # Category Pages
    path('programming-books/', views.programming_books, name='programming_books'),
    path('literature-books/', views.literature_books, name='literature_books'),
    path('science-books/', views.science_books, name='science_books'),
    path('business-books/', views.business_books, name='business_books'),
    path('engineering-books/', views.engineering_books, name='engineering_books'),
    path('history-books/', views.history_books, name='history_books'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage-books/', views.manage_books, name='manage_books'),
    path(
        'edit-book/<int:book_id>/',
        views.edit_book,
        name='edit_book'
    ),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('manage-librarians/', views.manage_librarians, name='manage_librarians'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path(
    'edit-category/<int:category_id>/',
    views.edit_category,
    name='edit_category'
),
    path('upload-books/', views.upload_books, name='upload_books'),
    path('librarian-categories/', views.librarian_categories, name='librarian_categories'),
    path('student-records/', views.student_records, name='student_records'),
    path('student_library/',views.student_library,name='student_library'),
    path('bookmarks/',views.bookmarks,name='bookmarks'),
    path(
    'add-bookmark/<int:book_id>/',
    views.add_bookmark,
    name='add_bookmark'
),
    path(
    'save-progress/<int:book_id>/',
    views.save_progress,
    name='save_progress'
),
    path(
    'read-book/<int:book_id>/',
    views.read_book,
    name='read_book'
),
    path(
    'reading-progress/',
    views.reading_progress,
    name='reading_progress'
),
path(
    'reading-activity/',
    views.reading_activity,
    name='reading_activity'
),
path(
    'save-page/',
    views.save_page,
    name='save_page'
),
path(
    'toggle-favorite/<int:book_id>/',
    views.toggle_favorite,
    name='toggle_favorite'
),

path(
    'favorite-books/',
    views.favorite_books,
    name='favorite_books'
),
    path('logout/', views.logout_view, name='logout'),
]