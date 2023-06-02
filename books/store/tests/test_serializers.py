from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTest(TestCase):
    def test_ok(self):
        user0 = User.objects.create(username='user0')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        book1 = Book.objects.create(name='Test Book1', price=25, author='Author1', owner=user0)
        book2 = Book.objects.create(name='Test Book2', price=55, author='Author2', owner=user2)

        UserBookRelation.objects.create(user=user0, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book1, like=True, rate=4)

        UserBookRelation.objects.create(user=user0, book=book2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),).order_by('name')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test Book1',
                'price': '25.00',
                'author': 'Author1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'user0',
                'readers': [
                    {
                        'first_name': '',
                        'last_name': '',
                    },
                    {
                        'first_name': '',
                        'last_name': '',
                    },
                    {
                        'first_name': '',
                        'last_name': '',
                    },
                ]
            },
            {
                'id': book2.id,
                'name': 'Test Book2',
                'price': '55.00',
                'author': 'Author2',
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': 'user2',
                'readers': [
                    {
                        'first_name': '',
                        'last_name': '',
                    },
                    {
                        'first_name': '',
                        'last_name': '',
                    },
                    {
                        'first_name': '',
                        'last_name': '',
                    },
                ]
            }
        ]
        print(expected_data)
        print(data)
        self.assertEqual(expected_data, data)
