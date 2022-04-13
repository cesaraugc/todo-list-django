import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .serializers import UserSerializer


client = APIClient()
User = get_user_model()


class UsersManagersTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            login='normal', 
            password='12345',
            name='Bruce Wayne', 
            email='anything@user.com'
        )
        self.assertEqual(user.name, 'Bruce Wayne')
        self.assertEqual(user.email, 'anything@user.com')
        self.assertEqual(user.login, 'normal')

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(login='', password="12345")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            name='Clark Kent', 
            email='super_anything@user.com',
            login='admin', 
            password='12345'
        )
        self.assertEqual(admin_user.name, 'Clark Kent')
        self.assertEqual(admin_user.email, 'super_anything@user.com')
        self.assertEqual(admin_user.login, 'admin')

        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                name='Clark Kent',
                email='super_anything@user.com', 
                login='admin', 
                password='12345', 
                is_superuser=False
            )

    def test_create_superuser_with_login_and_password_only(self):
        admin_user = User.objects.create_superuser(
            login='admin', 
            password='12345'
        )
        self.assertEqual(admin_user.login, 'admin')
        self.assertEqual(admin_user.name, '')
        self.assertEqual(admin_user.email, '')

        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class AuthorizationRequestTests(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(
            login='normal', 
            password='12345',
            name='Bruce Wayne', 
            email='anything@user.com'
        )
        self.valid_payload = {
            'login': user.login,
            'password': '12345'
        }
        
    def test_authorization(self):
        response = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class GetSingleUserTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            login='normal', 
            password='12345',
            name='Bruce Wayne', 
            email='anything@user.com'
        )
        
    def test_get_valid_single_user(self):
        client.force_authenticate(user=self.user)
        response = client.get(
            reverse(
                'get_update_user', 
                kwargs={"id": self.user.id}
            ),
        )
        searched_user = User.objects.get(id=self.user.id)
        serializer = UserSerializer(searched_user)
        self.assertEqual(response.data['user'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        client.force_authenticate(user=self.user)
        response = client.get(
            reverse(
                'get_update_user', 
                kwargs={"id": 1001}
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class createNewUserApiTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            login='normal', 
            password='12345',
            name='Bruce Wayne', 
            email='anything@user.com'
        )

        self.valid_payload = {
            'name': "User's name",
            'email': "any@user.com",
            'login': 'username',
            'password': '12345'
        }

        self.valid_payload_2 = {
            'name': "",
            'email': "",
            'login': 'username2',
            'password': '12345'
        }

        self.invalid_payload = {
            'name': "User's name 2",
            'email': "any2@user.com",
            'login': None,
            'password': '12345'
        }

    def test_create_valid_user(self):
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('post_user'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_valid_user_without_name_email(self):
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('post_user'),
            data=json.dumps(self.valid_payload_2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('post_user'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_existing_user(self):
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('post_user'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = client.post(
            reverse('post_user'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class UpdateSingleUserTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            login='normal', 
            password='12345',
            name='Bruce Wayne', 
            email='anything@user.com'
        )

        self.valid_payload = {
            'login': 'normal',
            'password': '12345678',
            'name': 'The New Bruce Wayne',
            'email': 'tnbw@user.com'
        }

        self.invalid_payload = {
            'login': None,
            'password': '12345678',
            'name': 'The New Bruce Wayne',
            'email': 'any@user.com'
        }

    def test_valid_update_user(self):
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse(
                'get_update_user', 
                kwargs={"id": self.user.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        refreshed_user = User.objects.get(id=self.user.id)
        self.assertEqual(refreshed_user.name, self.valid_payload['name'])
        self.assertEqual(refreshed_user.email, self.valid_payload['email'])
        self.assertEqual(refreshed_user.login, self.user.login)

    def test_invalid_update_user(self):
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse(
                'get_update_user', 
                kwargs={"id": self.user.id}
            ),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
