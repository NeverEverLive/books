from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializeTestCase(TestCase):

    def test_ok(self):
        user1 = User.objects.create(username='test_user1', first_name='Ivan', last_name='Petrov')
        user1_id = user1.id
        user2 = User.objects.create(username='test_user2', first_name='Ivan', last_name='Sidorov')
        user3 = User.objects.create(username='test_user3', first_name='1', last_name='2')
        book1 = Book.objects.create(name="test book 1", price=25,
                                         author_name='Author1', owner=user1)
        book2 = Book.objects.create(name="test book 2", price=35,
                                         author_name='Author2', owner=None)

        UserBookRelation.objects.create(user=user1, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book1, like=True, rate=5)
        user_book_3 = UserBookRelation.objects.create(user=user3, book=book1, like=True)
        user_book_3.rate = 4
        user_book_3.save()



        UserBookRelation.objects.create(user=user1, book=book2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        print(books[0].rating)
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'test book 1',
                'price': '25.00',
                'author_name': 'Author1',
                'owner': user1_id,
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'test_user1',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov',
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov',
                    },
                    {
                        'first_name': '1',
                        'last_name': '2',
                    },
                ]
            },
            {
                'id': book2.id,
                'name': 'test book 2',
                'price': '35.00',
                'author_name': 'Author2',
                'owner': None,
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov',
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov',
                    },
                    {
                        'first_name': '1',
                        'last_name': '2',
                    },
                ]
            },
        ]
        print(data)
        print(expected_data)
        self.assertEqual(expected_data, data)
