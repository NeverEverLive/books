from unittest import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializeTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name="test book 1", price=25)
        book2 = Book.objects.create(name="test book 2", price=35)

        data = BooksSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'test book 1',
                'price': '25.00'
            },
            {
                'id': book2.id,
                'name': 'test book 2',
                'price': '35.00'
            },
        ]
        self.assertEqual(expected_data, data)
