from rest_framework.decorators import action, api_view
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from auth_.models import Activation, MainUser
from auth_.message import send_html
from auth_.token import get_token
from auth_.serializers import (ActivationSerializer, EmailSerializer,
                               RegistrationSerializer, MainUserSerializer,
                               LoginSerializer,)
from utils import messages


class ActivationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Activation.objects.all()
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return EmailSerializer
        return ActivationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activation = serializer.create_activation()
        return Response({'activation': ActivationSerializer(activation).data})

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def activate(self, request, *args, **kwargs):
        try:
            activation = Activation.objects.get(uuid=request.data['uuid'])
        except Activation.DoesNotExist:
            raise ValidationError(messages.LINK_INVALID)
        activation.is_valid(raise_exception=True)
        serializer = RegistrationSerializer(data={'email': activation.email, 'password': activation.password})
        serializer.is_valid(raise_exception=True)
        user = serializer.complete(activation)
        return Response({'code': 0})


class UserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = MainUser.objects.all()
    http_method_names = ['post', 'get', 'patch']
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return MainUserSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_token(user)
        return Response({'user': MainUserSerializer(user).data, 'token': token})
