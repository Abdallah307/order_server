from django.urls import path
from .views import purchase_book

urlpatterns = [
    path('purchase/<int:book_id>', purchase_book, name='purchase-book')
]