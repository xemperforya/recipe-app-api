from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serilizer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only':True, 'min_length':5}}
    
    def create(self, validated_data):
        """
            create a new user with encrypted password and return it
        """
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializzer for the user token"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self, attr):
        """
            validate the given attributes
        """
        email = attr.get('email')
        password = attr.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = ('INVALID AUTHENTICATION CREDENTIALS')
            raise serializers.ValidationError(msg, code = 'authentication')

        attr['user'] = user
        return attr
