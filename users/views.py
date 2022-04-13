
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser as User
from .serializers import UserSerializer, MyTokenObtainPairSerializer


@api_view(['GET', 'PUT'])
def get_update_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response({"user": serializer.data})
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"user": serializer.data}, 
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def post_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"user": serializer.data}, 
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"error": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer