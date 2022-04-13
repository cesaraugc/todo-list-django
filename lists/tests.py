import json
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import List, Item
from .serializers import ListSerializer, ItemSerializer

User = get_user_model()
client = APIClient()


class GetSingleListTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_superuser(login='test', password='12345')
        self.first_list = List.objects.create(title="List 1")
        self.second_list = List.objects.create(title="List 2")
        self.third_list = List.objects.create(title="List 3")
        
    def test_get_valid_single_list(self):
        client.logout()
        response = client.get(
            reverse('get_delete_list', kwargs={"id": self.first_list.id})
        )
        list = List.objects.get(id=self.first_list.id)
        serializer = ListSerializer(list)
        self.assertEqual(response.data['list'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_list(self):
        client.logout()
        response = client.get(
            reverse('get_delete_list', kwargs={"id": 1001})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class createNewListTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_superuser(login='test', password='12345')

        self.valid_payload = {
            'title': 'List 1'
        }
        self.invalid_payload = {
            'title': ''
        }

    def test_create_valid_list(self):
        client.logout()
        response = client.post(
            reverse('post_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_list(self):
        client.logout()
        response = client.post(
            reverse('post_list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(login='test', password='12345')
        self.first_list = List.objects.create(title="List 1")
        self.second_list = List.objects.create(title="List 2")
    
    def test_unauthorized_delete_list(self):
        client.logout()
        response = client.delete(
            reverse(
                'get_delete_list', 
                kwargs={'id': self.first_list.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_valid_delete_list(self):
        client.force_authenticate(user=self.user)
        response = client.delete(
            reverse(
                'get_delete_list', 
                kwargs={'id': self.first_list.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_invalid_delete_list(self):
        client.force_authenticate(user=self.user)
        response = client.delete(
            reverse('get_delete_list', kwargs={'id': 1001})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GetAllItemsFromListTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_superuser(login='test', password='12345')
        self.list = List.objects.create(title="List 1")
        Item.objects.create(
            title="Item 1", 
            description="Item 1 Description",
            list=self.list,
            created_by=self.user
        )
        Item.objects.create(
            title="Item 2", 
            description="Item 2 Description",
            list=self.list,
            created_by=self.user
        )
        
    def test_get_all_items(self):
        client.force_authenticate(user=self.user)
        response = client.get(reverse('get_post_item', kwargs={"list_id": self.list.id}))
        items = Item.objects.filter(list=self.list).all()
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(response.data['items'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleItemTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_superuser(login='test', password='12345')
        self.list = List.objects.create(title="List 1")
        self.item = Item.objects.create(
            title="Item 1", 
            description="Item 1 Description",
            list=self.list,
            created_by=self.user
        )
        
    def test_get_valid_single_item(self):
        client.force_authenticate(user=self.user)
        response = client.get(
            reverse(
                'get_delete_update_item', 
                kwargs={"list_id": self.list.id, "id": self.item.id}
            )
        )
        item = Item.objects.get(id=self.item.id)
        serializer = ItemSerializer(item)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_item(self):
        client.force_authenticate(user=self.user)
        response = client.get(
            reverse(
                'get_delete_update_item', 
                kwargs={"list_id": self.list.id, "id": 1001}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class createNewItemTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_superuser(login='test', password='12345')
        self.list = List.objects.create(title="List 1")

        self.valid_payload = {
            'title': 'item 1 title',
            'description': 'item 1 description'
        }
        self.invalid_payload = {
            'title': '',
            'description': 'item 2 description'
        }

    def test_create_valid_item(self):
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('get_post_item', kwargs={"list_id": self.list.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_item(self):
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('get_post_item', kwargs={"list_id": self.list.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid_item_invalid_list(self):
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('get_post_item', kwargs={"list_id": 1001}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateSingleItemTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(login='test', password='12345')
        self.list = List.objects.create(title="List 1")
        self.item = Item.objects.create(
            title="Item 1", 
            description="Item 1 Description",
            list=self.list,
            created_by=self.user
        )
        self.valid_payload = {
            'title': 'item 1 new title',
            'description': 'item 1 new description'
        }
        self.invalid_payload = {
            'title': '',
            'description': 'item 1 new description'
        }

    def test_valid_update_item(self):
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse(
                'get_delete_update_item', 
                kwargs={"list_id": self.list.id, "id": self.item.id}
            ),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_item(self):
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse(
                'get_delete_update_item', 
                kwargs={"list_id": self.list.id, "id": self.item.id}
            ),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleItemTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(login='test', password='12345')
        self.list = List.objects.create(title="List 1")
        self.item = Item.objects.create(
            title="Item 1", 
            description="Item 1 Description",
            list=self.list,
            created_by=self.user
        )

    def test_valid_delete_list(self):
        client.force_authenticate(user=self.user)
        response = client.delete(
            reverse(
                'get_delete_update_item', 
                kwargs={"list_id": self.list.id, "id": self.item.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_list(self):
        client.force_authenticate(user=self.user)
        response = client.delete(
            reverse(
                'get_delete_update_item', 
                kwargs={"list_id": self.list.id, "id": 1001}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
