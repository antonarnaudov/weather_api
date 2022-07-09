from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from drf_writable_nested.serializers import WritableNestedModelSerializer

from core.models import Extended


class ExtendedSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Extended
        exclude = ('user', )


class UserSerializer(serializers.ModelSerializer):
    """
    Shows all fields for the User.
    Suitable for showing all User fields Default and Custom.
    """
    extended = ExtendedSerializer()

    class Meta:
        model = User
        exclude = ('password',)
        depth = 1


class UserSimpleSerializer(serializers.ModelSerializer):
    """
    Shows only id and username fields of the user.
    Suitable usage in other serializers where you dont need all the user data.
    """

    class Meta:
        model = User
        fields = ('id', 'username')


class RegisterSerializer(WritableNestedModelSerializer):
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
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        extended = validated_data.get('extended', {})
        extended = Extended.objects.create(
            user=user,
            phone=extended.get('phone', None)
        )
        extended.save()

        return user


class UpdateUserSerializer(WritableNestedModelSerializer):
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
