from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import UserBookRelation, Book


class SetRatingTestCase(TestCase):
    def setUp(self):
        user0 = User.objects.create(username='user0')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        self.book1 = Book.objects.create(name='Test Book1', price=25, author='Author1', owner=user0)

        UserBookRelation.objects.create(user=user0, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.book1)
        self.book1.refresh_from_db()
        self.assertEqual('4.67', str(self.book1.rating))
