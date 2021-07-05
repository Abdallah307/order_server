from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests

# Create your views here.


def query_book(book_id):
    try:
        response = requests.get(
            f'http://localhost:3000/catalog/info/{book_id}')
        return response
    except:
        raise requests.ConnectionError


def book_exists(status_code):
    if status_code == 200:
        return True
    return False


def book_available_in_stock(number_of_items):
    print(number_of_items)
    if number_of_items > 0:
        return True
    return False


def decrement_number_of_books(book_id):
    requests.put(f'http://localhost:3000/catalog/update/{book_id}')


@api_view(['POST'])
def purchase_book(request, book_id):
    try:
        response = query_book(book_id)

        if book_exists(response.status_code):
            book = response.json()
            if book_available_in_stock(book['number_of_items']):
                decrement_number_of_books(book_id)
                return Response({
                    "Message": "Book purchased successfully",
                    "book": response.json(),
                })

            return Response({
                "Message": "This Book is not available in the stock, sorry!"
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "Message": "This Book is not found"
        }, status=status.HTTP_404_NOT_FOUND)

    except requests.ConnectionError:
        return Response({
            "Message": "This service is not available right now"
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
