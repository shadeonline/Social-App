from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from django.conf import settings

from django.core.files import File
import os


class CreatePostTest(APITestCase):
    def setUp(self):
        #Login
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)

        # Open the image file and create a Django File object
        image_file = open(os.path.join(settings.BASE_DIR, 'social', 'static', 'images', 'user.png'), 'rb')

        django_file = File(image_file)

        # Define the post data, including the image file
        post_data = {
            'description': 'Test post',
            'image': django_file
        }
        # Send a POST request to the API
        response = self.client.post('/api/createpost/', post_data, format='multipart')

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        #Check if post is created
        self.assertEqual(Post.objects.count(), 1)

        #Check if post entries is same as what we posted
        post = Post.objects.first()
        self.assertEqual(post.description, 'Test post')
        self.assertEqual(post.user, self.user)

    def test_create_post_unauthenticated(self):
        self.client.force_authenticate(user=None)

        # Open the image file and create a Django File object
        image_file = open(os.path.join(settings.BASE_DIR, 'social', 'static', 'images', 'user.png'), 'rb')
        django_file = File(image_file)
        
        # Define the post data, including the image file
        post_data = {
            'description': 'Test post',
            'image': django_file
        }

        # Send a POST request to the API
        response = self.client.post('/api/createpost/', post_data, format='multipart')

        # Check that the response status code is 401 (redirect)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostListTest(APITestCase):
    def setUp(self):
        #Login
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def testURL(self):
        #Test if URL is valid
        url = reverse('posts_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list(self):
        # Create multiple posts with images
        for i in range(3):
            # Open the image file and create a Django File object
            image_file = open(os.path.join(settings.BASE_DIR, 'social', 'static', 'images', 'user.png'), 'rb')
            django_file = File(image_file)

            # Define the post data, including the image file
            post_data = {
                'description': f'Test post {i}',
                'image': django_file
            }

            # Send a POST request to create the post
            self.client.post('/api/createpost/', post_data, format='multipart')

        # Check if the posts are listed in the API response
        url = reverse('posts_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the number of posts listed in the API response matches the number of posts created
        self.assertEqual(len(response.data), Post.objects.count())

        # Check if all the posts have valid image URLs in the API response
        for post in response.data:
            self.assertIsNotNone(post['image'])
            self.assertTrue(post['image'].startswith('http://'))
        
        #Check if images returned equals 3 as posted earlier
        images_count = sum('image' in post for post in response.data)
        self.assertEqual(images_count, 3)

class UserListTest(APITestCase):
    def setUp(self):
        #Create 2 different users
        self.user1 = User.objects.create_user(
            username='testuser1', email='testuser1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(
            username='testuser2', email='testuser2@example.com', password='testpassword2')

    def testURL(self):
        #test if URL is valid
        url = reverse('users_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_users_list(self):
        #test if user list return 2 users that was created earlier
        url = reverse('users_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class UserDetailTest(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )

    def test_get_user_detail(self):
        # Retrieve the user detail using the API
        url = reverse('users_api', kwargs={'pk': self.user.pk})
        response = self.client.get(url)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data matches the expected data
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], self.user.username)




class UserSignupTest(APITestCase):
    def test_user_signup(self):
        # Define the user data to be submitted in the request
        user_data = {
            'username': 'tester',
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'Test',
            'last_name': 'User'
        }

        # Make a POST request to the signup API with the user data
        url = reverse('signup_api')
        response = self.client.post(url, user_data, format='multipart')

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Check that a user with the given username and email was created
        user = User.objects.get(username=user_data['username'])
        self.assertEqual(user.email, user_data['email'])

        # Check that the user is logged in
        self.assertTrue(self.client.login(username=user_data['username'], password=user_data['password']))


class UpdateProfileTest(APITestCase):
    def setUp(self):
        # Define the user data to be submitted in the request
        user_data = {
            'username': 'tester',
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'Test',
            'last_name': 'User'
        }
        # Make a POST request to the signup API with the user data
        self.client.post(reverse('signup_api'), user_data, format='multipart')
        # Log the user in
        self.client.login(username='tester', password='testpass')
        # Get user details
        self.user = User.objects.get(username='tester')

        #Set URL for test usage
        self.url = reverse('profile_update', args=[self.user.id])

    def test_get_profile(self):
        # Login user
        self.client.force_login(self.user)
        # Get response after login
        response = self.client.get(self.url)
        #Check if login works
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #Get expected data from serialzer
        expected_data = ProfileSerializer(self.user.profile).data
        #Check if profile complies with serializer
        self.assertEqual(response.data, expected_data)

    def test_update_profile(self):
        #Login user
        self.client.force_login(self.user)
        data = {
            'intro': 'Test intro'
        }
        #Post Update
        response = self.client.post(self.url, data)
        # Get response
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        #Check if user profile have been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.intro, 'Test intro')