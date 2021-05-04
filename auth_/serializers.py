import logging
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from auth_.models import MainUser, Activation
from auth_.message import send_html
from utils import messages


logger = logging.getLogger(__name__)


class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('email', 'timestamp')


class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activation
        fields = ('email', 'created_at', 'end_time', 'uuid')


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    def complete(self, activation):
        user = MainUser.objects.create_user(self.validated_data['email'], self.validated_data['password'])
        activation.is_active = False
        activation.save()
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    password1 = serializers.CharField(max_length=200)
    password2 = serializers.CharField(max_length=200)

    def validate(self, attrs):
        if Activation.objects.filter(email=attrs['email']).exists():
            logger.warning(messages.USER_EXISTS)
            raise ValidationError(messages.USER_EXISTS)
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(messages.PASSWORD_NOT_SAME)
        return attrs

    def create_activation(self):
        activation = Activation.objects.create(email=self.validated_data['email'], password=self.validated_data['password1'])
        activation.save()
        # send_html(activation, self.context['request'])
        return activation


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = MainUser.objects.get(email=attrs['email'])
        except MainUser.DoesNotExist:
            raise ValidationError(messages.USER_DOESNOTEXIST)
        if not check_password(attrs['password'], user.password):
            raise ValidationError(messages.USER_DOESNOTEXIST)
        attrs['user'] = user
        return attrs
