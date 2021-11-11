from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(name="test book 1", price=25, author_name='Author 1')
        self.book2 = Book.objects.create(name="test book 2", price=55, author_name='Author 5')
        self.book3 = Book.objects.create(name="test book Author 1", price=55, author_name='Author 2')

    def test_get(self):
        url = reverse('book-list')  # book-detail for one book
        print(url)
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

        print(response)
        print(response.data)

    def test_get_filter(self):
        url = reverse('book-list')  # book-detail
        print(url)
        response = self.client.get(url, data={'price': 55})
        serializer_data = BooksSerializer([self.book2, self.book3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

        print(response)
        print(response.data)

    def test_get_search(self):
        url = reverse('book-list')  # book-detail
        print(url)
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book1, self.book3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

        print(response)
        print(response.data)

    def test_get_order(self):
        url = reverse('book-list')  # book-detail
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BooksSerializer([self.book1, self.book2, self.book3], many=True).data
        print(serializer_data)
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

