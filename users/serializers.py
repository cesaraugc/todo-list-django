from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser as User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['login', 'name', 'email', 'password']
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True},
            'password': {'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        data = {
            'login': validated_data.get('login', instance.login),
            'password': validated_data.get('password', instance.password),
            'name': validated_data.get('name', instance.name),
            'email': validated_data.get('email', instance.email)
        }
        return User.objects.update_user(user=instance, **data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        serializer = UserSerializer(user)
        # token['user'] = serializer.data
        token.__setitem__('user', serializer.data)
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        # data['refresh'] = str(refresh)
        data['token'] = str(refresh.access_token)
        data.pop('refresh')
        data.pop('access')
        serializer = UserSerializer(self.user)
        data['user'] = serializer.data
        return data
