from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post
from rest_framework_simplejwt.tokens import RefreshToken

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='newuser', password='password123')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post content.')
        self.assertEqual(self.post.author.username, 'newuser')

class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='newuser', password='password123')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='This is a test comment.'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, 'This is a test comment.')
        self.assertEqual(self.comment.post.title, 'Test Post')
        self.assertEqual(self.comment.author.username, 'newuser')


class PostAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='newuser', password='password123')
        self.token = self._get_token_for_user(self.user)
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )

    def _get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_get_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post_authenticated(self):
        data = {
            'title': 'New Post',
            'content': 'Content for the new post.',
            'author': 'newuser'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post('/api/posts/', data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Post')

    def test_create_post_unauthenticated(self):
        data = {
            'title': 'New Post',
            'content': 'Content for the new post.'
        }
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
