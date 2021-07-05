from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .models import Order
import datetime

# Create your views here.


def query_book(book_id):
    try:
        response = requests.get(
            f'https://bazar-store-catalog.herokuapp.com/catalog/info/{book_id}')
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
    requests.put(f'https://bazar-store-catalog.herokuapp.com/catalog/update/{book_id}')


def store_order(book_id):
    order = Order(book_id=book_id)
    order.save()
    return


@api_view(['POST'])
def purchase_book(request, book_id):
    '''
    purchase_book Function:
        purchase a book with the specified id


        Parameter:
            book_id : book id

        Return:
            returns a successfull message alongside with the purchased book info    
    '''

    try:
        response = query_book(book_id)

        if book_exists(response.status_code):
            book = response.json()
            if book_available_in_stock(book['number_of_items']):
                decrement_number_of_books(book_id)
                store_order(book_id)
                return Response({
                    "Message": "Book purchased successfully",
                    "book": book
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
