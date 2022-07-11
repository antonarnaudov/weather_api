from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from drf_writable_nested.serializers import WritableNestedModelSerializer

from core.models import Extended


class ExtendedSerializer(WritableNestedModelSerializer):
    """
    Extended User writable serializer
    Suitable only for nesting in other serializers
    """

    class Meta:
        model = Extended
        exclude = ('user',)  # Excludes duplicating user field


class UserSerializer(serializers.ModelSerializer):
    """
    Shows all fields for the User.
    Suitable for showing all User fields Default and Custom.
    """
    extended = ExtendedSerializer()

    class Meta:
        model = User
        exclude = ('password',)  # excludes password for security reasons
        depth = 1  # Shows detailed Extended serializer information


class UserSimpleSerializer(serializers.ModelSerializer):
    """
    Shows only id and username fields of the user.
    Suitable usage in other serializers where you dont need all the user data.
    """

    class Meta:
        model = User
        fields = ('id', 'username')


class RegisterSerializer(WritableNestedModelSerializer):
    """
    This serializer provides validation and serialization for new User and Extended objects
    """

    # Sets all necesery fields and their options and validations
    extended = ExtendedSerializer(required=False)

    email = serializers.EmailField(
        required=False,
        default='',
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(default='', required=False, allow_blank=True)
    last_name = serializers.CharField(default='', required=False, allow_blank=True)

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'extended')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False}
        }

    def validate(self, attrs):
        """Applying additional validation"""

        # Checks if passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """
        Creates User and Extended objects

        :param validated_data: request data - post validation
        :return: User
        """
        # Creates User account
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        # Creates Extended attached to the User
        extended = validated_data.get('extended', {})  # If extended not passed in the request - set it to {}
        extended = Extended.objects.create(
            user=user,
            phone=extended.get('phone', None)  # If no phone in data, set field to None
        )
        extended.save()

        return user


class UpdateUserSerializer(WritableNestedModelSerializer):
    """Provides all user fields including extended, except for password"""
    extended = ExtendedSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'extended')
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False}
        }
