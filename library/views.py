from django.shortcuts import render , get_object_or_404
from .models import Book, Category
from django.db.models import Q
from .models import Book, Category , Review

def home(request):
    popular_books = Book.objects.filter(is_available=True)[:8]
    new_books = Book.objects.filter(is_available=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
  
    context = {
        'popular_books': popular_books,
        'new_books': new_books,
        'categories': categories,
    }
    return render(request, 'library/home.html', context)

def search(request):
    query = request.GET.get('q', '')
    results = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(category__name__icontains=query)
    ) if query else []
    
    return render(request, 'library/search.html', {
        'results': results,
        'query': query
    })


# این تابع جدید را به انتها اضافه کنید:
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    
    context = {
        'book': book,
        'reviews': reviews,
    }
    return render(request, 'library/book_detail.html', context)
