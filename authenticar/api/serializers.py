from users.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class User_serializer(serializers.Serializer):
    token_id = serializers.CharField()


class UserRegistroView(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()
    gmail = serializers.EmailField()
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    avatar = serializers.ImageField()

class serializer_update(serializers.Serializer):
    username = serializers.CharField()
    gmail = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('las contraseñas no son iguales')
        return data
    

class LoginZerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
