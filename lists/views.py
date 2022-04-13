from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item, List
from .serializers import ItemSerializer, ListSerializer
from .permissions import CantDeletePermissionClass


@api_view(['GET', 'DELETE'])
@permission_classes([CantDeletePermissionClass])
def get_delete_list(request, id):
    try:
        list = List.objects.get(id=id)
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ListSerializer(list)
        return Response(
            {
                "list": serializer.data, 
                "user_id": request.user.id
            }
        )
    elif request.method == 'DELETE':
        list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def post_list(request):
    data = {
        'title': request.data.get('title')
    }
    serializer = ListSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"list": serializer.data}, 
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_item(request, list_id, id):
    try:
        list = List.objects.get(id=list_id)
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'list': list_id,
            'created_by': request.user.id
        }
        serializer = ItemSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"item": serializer.data}, 
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == 'DELETE':
        item.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['GET', 'POST'])
def get_post_item(request, list_id):

    try:
        list = List.objects.get(id=list_id)
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        items = Item.objects.filter(list=list).all()
        serializer = ItemSerializer(items, many=True)
        return Response({"items": serializer.data})

    elif request.method == 'POST':
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'list': list_id,
            'created_by': request.user.id
        }
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"item": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )